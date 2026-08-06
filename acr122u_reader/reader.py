import json
import os
import signal
import sys
import time
from typing import Optional

import requests
from smartcard.CardMonitoring import CardMonitor, CardObserver
from smartcard.util import toHexString


GET_UID = [0xFF, 0xCA, 0x00, 0x00, 0x00]
SUPERVISOR_TOKEN = os.environ.get("SUPERVISOR_TOKEN")
RESTART_FLAG = "/data/home_assistant_restart_required"
RESTART_NOTIFICATION_ID = "ha_usb_nfc_restart_required"

last_uid: Optional[str] = None
last_scan_time = 0.0


def read_options() -> dict:
    try:
        with open("/data/options.json", "r", encoding="utf-8") as file:
            return json.load(file)
    except (FileNotFoundError, json.JSONDecodeError):
        return {}


options = read_options()
cooldown_seconds = float(options.get("cooldown_seconds", 2))


def send_event(event_type: str, payload: dict) -> None:
    if not SUPERVISOR_TOKEN:
        print("SUPERVISOR_TOKEN is unavailable", flush=True)
        return

    try:
        response = requests.post(
            f"http://supervisor/core/api/events/{event_type}",
            headers={
                "Authorization": f"Bearer {SUPERVISOR_TOKEN}",
                "Content-Type": "application/json",
            },
            json=payload,
            timeout=10,
        )
        response.raise_for_status()
        print(f"Sent {event_type}: {payload}", flush=True)
    except requests.RequestException as error:
        print(f"Failed to send {event_type}: {error}", flush=True)


def send_restart_notification() -> None:
    """Create a persistent notification when the bundled integration changed."""
    if not os.path.exists(RESTART_FLAG):
        return

    if not SUPERVISOR_TOKEN:
        print("Cannot create restart notification: SUPERVISOR_TOKEN unavailable", flush=True)
        return

    url = "http://supervisor/core/api/services/persistent_notification/create"
    payload = {
        "title": "Restart Home Assistant required",
        "message": (
            "ha-usb-nfc installed or updated its bundled ACR122U integration. "
            "Restart Home Assistant Core, then add or reload the "
            "ACR122U NFC Reader integration under Settings → Devices & services."
        ),
        "notification_id": RESTART_NOTIFICATION_ID,
    }

    for attempt in range(1, 31):
        try:
            response = requests.post(
                url,
                headers={
                    "Authorization": f"Bearer {SUPERVISOR_TOKEN}",
                    "Content-Type": "application/json",
                },
                json=payload,
                timeout=10,
            )
            response.raise_for_status()
            os.remove(RESTART_FLAG)
            print("Created Home Assistant restart-required notification", flush=True)
            return
        except (requests.RequestException, OSError) as error:
            if attempt == 30:
                print(
                    f"Failed to create restart notification after {attempt} attempts: {error}",
                    flush=True,
                )
                return
            time.sleep(2)


class NFCObserver(CardObserver):
    def update(self, observable, actions) -> None:
        global last_uid, last_scan_time

        added_cards, removed_cards = actions

        for card in added_cards:
            try:
                connection = card.createConnection()
                connection.connect()

                response, sw1, sw2 = connection.transmit(GET_UID)

                if (sw1, sw2) != (0x90, 0x00):
                    print(
                        f"UID command failed: SW1={sw1:02X}, SW2={sw2:02X}",
                        flush=True,
                    )
                    continue

                uid = toHexString(response).replace(" ", "").upper()
                now = time.monotonic()

                if uid == last_uid and now - last_scan_time < cooldown_seconds:
                    continue

                last_uid = uid
                last_scan_time = now

                print(f"Card placed: {uid}", flush=True)
                send_event(
                    "acr122u_card_present",
                    {"uid": uid, "reader": "ACR122U"},
                )

            except Exception as error:
                print(f"Card insertion error: {error}", flush=True)

        for _card in removed_cards:
            if last_uid:
                uid = last_uid
                print(f"Card removed: {uid}", flush=True)
                send_event(
                    "acr122u_card_removed",
                    {"uid": uid, "reader": "ACR122U"},
                )
                last_uid = None


def shutdown_handler(signum, frame) -> None:
    print("Stopping NFC reader...", flush=True)
    sys.exit(0)


def main() -> None:
    signal.signal(signal.SIGTERM, shutdown_handler)
    signal.signal(signal.SIGINT, shutdown_handler)

    send_restart_notification()

    print("Waiting for ACR122U and NFC cards...", flush=True)

    monitor = CardMonitor()
    observer = NFCObserver()
    monitor.addObserver(observer)

    try:
        while True:
            time.sleep(1)
    finally:
        monitor.deleteObserver(observer)


if __name__ == "__main__":
    main()
