from pathlib import Path

APP_NAME = "ha-usb-nfc"
APP_VERSION = "1.5.1"

SUPERVISOR_BASE_URL = "http://supervisor/core/api"
EVENT_CARD_PRESENT = "acr122u_card_present"
EVENT_CARD_REMOVED = "acr122u_card_removed"

READER_VENDOR_ID = "072f"
READER_PRODUCT_ID = "2200"
READER_NAME = "ACS ACR122U"

GET_UID = [0xFF, 0xCA, 0x00, 0x00, 0x00]

INTEGRATION_SOURCE = Path("/opt/acr122u_integration")
INTEGRATION_TARGET = Path("/homeassistant/custom_components/acr122u")
INTEGRATION_RESTART_FLAG = Path("/data/home_assistant_restart_required")

NOTIFICATION_PROTECTION = "ha_usb_nfc_protection_mode"
NOTIFICATION_NO_READER = "ha_usb_nfc_reader_missing"
NOTIFICATION_RESTART = "ha_usb_nfc_restart_required"
