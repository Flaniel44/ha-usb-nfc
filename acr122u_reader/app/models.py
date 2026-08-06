from dataclasses import dataclass
from typing import Optional


@dataclass
class ReaderState:
    connected: bool = False
    present: bool = False
    current_uid: Optional[str] = None
    last_uid: Optional[str] = None
