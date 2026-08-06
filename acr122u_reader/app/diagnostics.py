import subprocess
from dataclasses import dataclass

from smartcard.System import readers

from .constants import (
    APP_NAME,
    APP_VERSION,
    READER_PRODUCT_ID,
    READER_VENDOR_ID,
)
from .errors import HUN_001, HUN_002
from .events import HomeAssistantClient
from .notifications import NotificationManager


@dataclass
class DiagnosticResult:
    reader_detected: bool
    reader_openable: bool


def print_banner() -> None:
    print("────────────────────────────────────", flush=True)
    print(f"{APP_NAME} v{APP_VERSION}", flush=True)
    print("────────────────────────────────────", flush=True)
    print("Running startup diagnostics...", flush=True)


def usb_reader_detected() -> bool:
    try:
        result = subprocess.run(
            ["lsusb", "-d", f"{READER_VENDOR_ID}:{READER_PRODUCT_ID}"],
            capture_output=True,
            text=True,
            timeout=5,
            check=False,
        )
        return result.returncode == 0 and bool(result.stdout.strip())
    except (OSError, subprocess.SubprocessError):
        return False


def pcsc_reader_openable() -> bool:
    try:
        return any("ACR122" in str(reader) for reader in readers())
    except Exception:
        return False


def run_diagnostics(
    client: HomeAssistantClient,
    notifications: NotificationManager,
) -> DiagnosticResult:
    if client.available:
        print("✓ Home Assistant API token available", flush=True)
    else:
        print("✗ Home Assistant API token unavailable", flush=True)

    detected = usb_reader_detected()
    if not detected:
        print("✗ Supported USB NFC reader not detected [HUN-002]", flush=True)
        notifications.show_error("ha_usb_nfc_reader_missing", HUN_002)
        return DiagnosticResult(False, False)

    print("✓ ACR122U detected on USB", flush=True)
    notifications.dismiss("ha_usb_nfc_reader_missing")

    openable = pcsc_reader_openable()
    if not openable:
        print("✗ ACR122U cannot be opened [HUN-001]", flush=True)
        print("  Likely cause: Protection mode is enabled", flush=True)
        notifications.show_error("ha_usb_nfc_protection_mode", HUN_001)
        return DiagnosticResult(True, False)

    print("✓ USB permissions and PC/SC access OK", flush=True)
    notifications.dismiss("ha_usb_nfc_protection_mode")
    return DiagnosticResult(True, True)
