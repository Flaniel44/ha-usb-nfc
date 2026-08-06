from dataclasses import dataclass


@dataclass(frozen=True)
class HealthError:
    code: str
    title: str
    message: str


HUN_001 = HealthError(
    code="HUN-001",
    title="USB reader access denied",
    message=(
        "ha-usb-nfc detected the ACR122U but could not open it. "
        "Protection mode is probably enabled. Open the app, disable "
        "Protection mode, and restart the app."
    ),
)

HUN_002 = HealthError(
    code="HUN-002",
    title="USB NFC reader not detected",
    message=(
        "ha-usb-nfc could not find a supported USB NFC reader. "
        "Connect the ACR122U and restart the app."
    ),
)

HUN_004 = HealthError(
    code="HUN-004",
    title="Home Assistant API unavailable",
    message=(
        "ha-usb-nfc could not reach the Home Assistant API. "
        "The app will keep retrying automatically."
    ),
)

HUN_005 = HealthError(
    code="HUN-005",
    title="Integration installation failed",
    message=(
        "ha-usb-nfc could not install the bundled Home Assistant integration. "
        "Check that the app has write access to the Home Assistant configuration directory."
    ),
)
