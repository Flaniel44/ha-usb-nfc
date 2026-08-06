from __future__ import annotations

import threading
import time
from typing import Any

from smartcard.CardMonitoring import CardMonitor, CardObserver
from smartcard.Exceptions import CardConnectionException, NoCardException
from smartcard.util import toHexString

from .constants import EVENT_CARD_PRESENT, EVENT_CARD_REMOVED, GET_UID
from .events import HomeAssistantClient
from .models import ReaderState


class NFCObserver(CardObserver):
    def __init__(
        self,
        client: HomeAssistantClient,
        state: ReaderState,
        cooldown_seconds: float,
        removal_poll_interval: float,
    ) -> None:
        self._client = client
        self._state = state
        self._cooldown_seconds = cooldown_seconds
        self._removal_poll_interval = max(0.05, removal_poll_interval)
        self._last_scan_time = 0.0

        self._lock = threading.Lock()
        self._active_connection: Any | None = None
        self._presence_thread: threading.Thread | None = None
        self._stop_presence = threading.Event()

    def update(self, observable, actions) -> None:
        added_cards, removed_cards = actions

        for card in added_cards:
            self._handle_added(card)

        if removed_cards:
            self._mark_removed("PC/SC removal event")

    def _handle_added(self, card) -> None:
        try:
            connection = card.createConnection()
            connection.connect()

            response, sw1, sw2 = connection.transmit(GET_UID)
            if (sw1, sw2) != (0x90, 0x00):
                print(
                    f"✗ UID command failed: SW1={sw1:02X}, SW2={sw2:02X}",
                    flush=True,
                )
                return

            uid = toHexString(response).replace(" ", "").upper()
            now = time.monotonic()

            with self._lock:
                if (
                    uid == self._state.current_uid
                    and now - self._last_scan_time < self._cooldown_seconds
                ):
                    return

                self._last_scan_time = now
                self._state.present = True
                self._state.current_uid = uid
                self._state.last_uid = uid
                self._active_connection = connection

            print(f"Card placed: {uid}", flush=True)
            self._client.send_event(
                EVENT_CARD_PRESENT,
                {"uid": uid, "reader": "ACR122U"},
            )
            self._start_presence_monitor()

        except Exception as error:
            print(f"✗ Card insertion error: {error}", flush=True)

    def _start_presence_monitor(self) -> None:
        self._stop_presence.set()

        old_thread = self._presence_thread
        if old_thread and old_thread.is_alive():
            old_thread.join(timeout=0.5)

        self._stop_presence = threading.Event()
        self._presence_thread = threading.Thread(
            target=self._monitor_presence,
            name="acr122u-presence-monitor",
            daemon=True,
        )
        self._presence_thread.start()

    def _monitor_presence(self) -> None:
        while not self._stop_presence.wait(self._removal_poll_interval):
            with self._lock:
                connection = self._active_connection
                uid = self._state.current_uid

            if connection is None or uid is None:
                return

            try:
                _response, sw1, sw2 = connection.transmit(GET_UID)
                if (sw1, sw2) != (0x90, 0x00):
                    self._mark_removed(
                        f"presence poll returned {sw1:02X}{sw2:02X}"
                    )
                    return
            except (CardConnectionException, NoCardException, Exception) as error:
                self._mark_removed(f"presence poll failed: {error}")
                return

    def _mark_removed(self, reason: str) -> None:
        with self._lock:
            uid = self._state.current_uid
            if not uid or not self._state.present:
                return

            self._state.present = False
            self._state.current_uid = None
            self._active_connection = None

        self._stop_presence.set()

        print(f"Card removed: {uid} ({reason})", flush=True)
        self._client.send_event(
            EVENT_CARD_REMOVED,
            {"uid": uid, "reader": "ACR122U"},
        )

    def stop(self) -> None:
        self._stop_presence.set()
        thread = self._presence_thread
        if thread and thread.is_alive():
            thread.join(timeout=1)


class ReaderService:
    def __init__(
        self,
        client: HomeAssistantClient,
        cooldown_seconds: float,
        removal_poll_interval: float,
    ) -> None:
        self._state = ReaderState(connected=True)
        self._monitor = CardMonitor()
        self._observer = NFCObserver(
            client,
            self._state,
            cooldown_seconds,
            removal_poll_interval,
        )

    def run(self) -> None:
        self._monitor.addObserver(self._observer)
        print("✓ Reader service started", flush=True)
        print(
            "✓ Fast removal polling enabled "
            f"({self._observer._removal_poll_interval:.2f}s)",
            flush=True,
        )
        print("Waiting for NFC cards...", flush=True)

        try:
            while True:
                time.sleep(1)
        finally:
            self._observer.stop()
            self._monitor.deleteObserver(self._observer)
