from __future__ import annotations

import threading
import time

from smartcard.CardMonitoring import CardMonitor, CardObserver
from smartcard.scard import (
    SCARD_E_TIMEOUT,
    SCARD_SCOPE_SYSTEM,
    SCARD_STATE_CHANGED,
    SCARD_STATE_EMPTY,
    SCARD_STATE_PRESENT,
    SCARD_S_SUCCESS,
    SCardEstablishContext,
    SCardGetErrorMessage,
    SCardGetStatusChange,
    SCardReleaseContext,
)
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
        self._presence_thread: threading.Thread | None = None
        self._stop_presence = threading.Event()

    def update(self, observable, actions) -> None:
        added_cards, removed_cards = actions

        for card in added_cards:
            self._handle_added(card)

        if removed_cards:
            self._mark_removed("PC/SC CardMonitor callback")

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
            reader_name = str(card.reader)
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

            print(f"Card placed: {uid}", flush=True)
            self._client.send_event(
                EVENT_CARD_PRESENT,
                {"uid": uid, "reader": reader_name},
            )
            self._start_presence_monitor(reader_name)

        except Exception as error:
            print(f"✗ Card insertion error: {error}", flush=True)

    def _start_presence_monitor(self, reader_name: str) -> None:
        self._stop_presence.set()

        old_thread = self._presence_thread
        if (
            old_thread
            and old_thread.is_alive()
            and old_thread is not threading.current_thread()
        ):
            old_thread.join(timeout=0.5)

        self._stop_presence = threading.Event()
        self._presence_thread = threading.Thread(
            target=self._monitor_reader_state,
            args=(reader_name, self._stop_presence),
            name="usb-nfc-reader-state-monitor",
            daemon=True,
        )
        self._presence_thread.start()

    def _monitor_reader_state(
        self,
        reader_name: str,
        stop_event: threading.Event,
    ) -> None:
        result, context = SCardEstablishContext(SCARD_SCOPE_SYSTEM)
        if result != SCARD_S_SUCCESS:
            print(
                "✗ Could not establish PC/SC status context: "
                f"{SCardGetErrorMessage(result)}",
                flush=True,
            )
            return

        timeout_ms = max(50, int(self._removal_poll_interval * 1000))
        states = [(reader_name, SCARD_STATE_PRESENT)]

        try:
            while not stop_event.is_set():
                result, new_states = SCardGetStatusChange(
                    context,
                    timeout_ms,
                    states,
                )

                if result == SCARD_E_TIMEOUT:
                    continue

                if result != SCARD_S_SUCCESS:
                    print(
                        "✗ Reader-state check failed: "
                        f"{SCardGetErrorMessage(result)}",
                        flush=True,
                    )
                    return

                if not new_states:
                    continue

                _reader, event_state, _atr = new_states[0]

                if event_state & SCARD_STATE_EMPTY:
                    self._mark_removed("reader state changed to empty")
                    return

                # Feed the observed state back into the next status-change call.
                states = [
                    (
                        reader_name,
                        event_state & ~SCARD_STATE_CHANGED,
                    )
                ]
        finally:
            SCardReleaseContext(context)

    def _mark_removed(self, reason: str) -> None:
        with self._lock:
            uid = self._state.current_uid
            if not uid or not self._state.present:
                return

            self._state.present = False
            self._state.current_uid = None

        self._stop_presence.set()

        print(f"Card removed: {uid} ({reason})", flush=True)
        self._client.send_event(
            EVENT_CARD_REMOVED,
            {"uid": uid, "reader": "USB NFC Reader"},
        )

    def stop(self) -> None:
        self._stop_presence.set()
        thread = self._presence_thread
        if (
            thread
            and thread.is_alive()
            and thread is not threading.current_thread()
        ):
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
            "✓ Non-blocking removal monitoring enabled "
            f"({self._observer._removal_poll_interval:.2f}s timeout)",
            flush=True,
        )
        print("Waiting for NFC cards...", flush=True)

        try:
            while True:
                time.sleep(1)
        finally:
            self._observer.stop()
            self._monitor.deleteObserver(self._observer)
