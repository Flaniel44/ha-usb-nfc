import os
import signal
import sys
import time

from .constants import (
    INTEGRATION_RESTART_FLAG,
    NOTIFICATION_RESTART,
)
from .diagnostics import print_banner, run_diagnostics
from .events import HomeAssistantClient
from .integration import install_integration
from .notifications import NotificationManager
from .options import read_options
from .reader import ReaderService


def shutdown_handler(signum, frame) -> None:
    print("Stopping ha-usb-nfc...", flush=True)
    sys.exit(0)


def show_restart_notification(
    client: HomeAssistantClient,
) -> None:
    if not INTEGRATION_RESTART_FLAG.exists():
        return

    for attempt in range(30):
        if client.create_notification(
            NOTIFICATION_RESTART,
            "Restart Home Assistant required",
            (
                "ha-usb-nfc installed or updated its bundled integration. "
                "Restart Home Assistant Core, then add or reload the "
                "ha-usb-nfc integration under Settings → Devices & services."
            ),
        ):
            try:
                INTEGRATION_RESTART_FLAG.unlink()
            except OSError:
                pass
            print("✓ Created restart-required notification", flush=True)
            return

        time.sleep(2)


def main() -> None:
    signal.signal(signal.SIGTERM, shutdown_handler)
    signal.signal(signal.SIGINT, shutdown_handler)

    print_banner()

    options = read_options()
    cooldown_seconds = float(options.get("cooldown_seconds", 2))

    client = HomeAssistantClient()
    notifications = NotificationManager(client)

    install_integration(notifications)
    show_restart_notification(client)

    result = run_diagnostics(client, notifications)
    if not result.reader_openable:
        print("Waiting for configuration to be corrected...", flush=True)
        while True:
            time.sleep(60)

    ReaderService(client, cooldown_seconds).run()


if __name__ == "__main__":
    main()
