from datetime import datetime, timezone
import time


def wall_timestamp() -> str:
    return datetime.now(timezone.utc).astimezone().isoformat(timespec="milliseconds")


def monotonic_ms() -> int:
    return int(time.monotonic() * 1000)


def log(message: str) -> None:
    print(f"{wall_timestamp()} | {message}", flush=True)
