import shutil

from .constants import (
    INTEGRATION_RESTART_FLAG,
    INTEGRATION_SOURCE,
    INTEGRATION_TARGET,
)
from .errors import HUN_005
from .notifications import NotificationManager


def install_integration(notifications: NotificationManager) -> bool:
    try:
        changed = (
            not INTEGRATION_TARGET.exists()
            or _directories_differ(INTEGRATION_SOURCE, INTEGRATION_TARGET)
        )

        if not changed:
            print("✓ Bundled integration is current", flush=True)
            return False

        print("• Installing/updating bundled integration...", flush=True)
        if INTEGRATION_TARGET.exists():
            shutil.rmtree(INTEGRATION_TARGET)

        INTEGRATION_TARGET.parent.mkdir(parents=True, exist_ok=True)
        shutil.copytree(INTEGRATION_SOURCE, INTEGRATION_TARGET)
        INTEGRATION_RESTART_FLAG.touch()

        print("⚠ Home Assistant Core restart required", flush=True)
        return True

    except OSError as error:
        print(f"✗ Integration installation failed: {error}", flush=True)
        notifications.show_error("ha_usb_nfc_integration_failed", HUN_005)
        return False


def _directories_differ(source, target) -> bool:
    source_files = {
        path.relative_to(source): path.read_bytes()
        for path in source.rglob("*")
        if path.is_file()
    }
    target_files = {
        path.relative_to(target): path.read_bytes()
        for path in target.rglob("*")
        if path.is_file()
    }
    return source_files != target_files
