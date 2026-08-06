import time
from typing import Optional

from smartcard.CardMonitoring import CardMonitor, CardObserver
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
    ) -> None:
        self._client = client
        self._state = state
        self._cooldown_seconds = cooldown_seconds
        self._last_scan_time = 0.0

    def update(self, observable, actions) -> None:
        added_cards, removed_cards = actions

        for card in added_cards:
            self._handle_added(card)

        for _card in removed_cards:
            self._handle_removed()

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

            if (
                uid == self._state.current_uid
                and now - self._last_scan_time < self._cooldown_seconds
            ):
                return

            self._last_scan_time = now
            self._state.present = True
            self._state.current_uid = uid
            self._state.last_uid = uid

            print(f"Card placed: {uid}", flush=True)
            self._client.send_event(
                EVENT_CARD_PRESENT,
                {"uid": uid, "reader": "ACR122U"},
            )

        except Exception as error:
            print(f"✗ Card insertion error: {error}", flush=True)

    def _handle_removed(self) -> None:
        uid = self._state.current_uid
        if not uid:
            return

        self._state.present = False
        self._state.current_uid = None

        print(f"Card removed: {uid}", flush=True)
        self._client.send_event(
            EVENT_CARD_REMOVED,
            {"uid": uid, "reader": "ACR122U"},
        )


class ReaderService:
    def __init__(
        self,
        client: HomeAssistantClient,
        cooldown_seconds: float,
    ) -> None:
        self._state = ReaderState(connected=True)
        self._monitor = CardMonitor()
        self._observer = NFCObserver(
            client,
            self._state,
            cooldown_seconds,
        )

    def run(self) -> None:
        self._monitor.addObserver(self._observer)
        print("✓ Reader service started", flush=True)
        print("Waiting for NFC cards...", flush=True)

        try:
            while True:
                time.sleep(1)
        finally:
            self._monitor.deleteObserver(self._observer)
