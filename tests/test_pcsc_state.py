"""Tests for PC/SC state monitoring helpers."""

from unittest import TestCase

from app.pcsc_state import acknowledge_reader_states


class ReaderStateTests(TestCase):
    """Verify that PC/SC transitions are acknowledged correctly."""

    def test_clears_changed_and_preserves_reader_state(self) -> None:
        changed = 0x0002
        present = 0x0020
        event_counter = 0x12340000

        self.assertEqual(
            acknowledge_reader_states(
                [("ACR122U", event_counter | changed | present, b"atr")],
                changed,
            ),
            [("ACR122U", event_counter | present, b"atr")],
        )

    def test_does_not_mutate_returned_states(self) -> None:
        states = [("ACR122U", 0x0012, b"")]

        acknowledge_reader_states(states, 0x0002)

        self.assertEqual(states, [("ACR122U", 0x0012, b"")])
