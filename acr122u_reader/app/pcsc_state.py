"""Helpers for advancing PC/SC reader-state monitoring."""

from collections.abc import Iterable
from typing import Any


def acknowledge_reader_states(
    states: Iterable[tuple[str, int, Any]],
    changed_mask: int,
) -> list[tuple[str, int, Any]]:
    """Convert event states into current states for the next PC/SC call.

    SCARD_STATE_CHANGED describes the transition returned by PC/SC. It must
    not be reported back as part of the state the application believes to be
    current. All other bits, including pcsc-lite's upper event counter, are
    retained.
    """
    return [
        (reader, event_state & ~changed_mask, atr)
        for reader, event_state, atr in states
    ]
