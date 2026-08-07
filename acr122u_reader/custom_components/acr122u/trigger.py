from __future__ import annotations

from typing import Any, cast

import voluptuous as vol

from homeassistant.const import CONF_OPTIONS, CONF_TARGET
from homeassistant.core import CALLBACK_TYPE, Event, HomeAssistant, callback
from homeassistant.helpers import config_validation as cv
from homeassistant.helpers.trigger import Trigger, TriggerActionRunner, TriggerConfig
from homeassistant.helpers.typing import ConfigType

from .const import EVENT_DEVICE_ACTIVITY

CONF_TAG_ID = "tag_id"

_CONFIG_SCHEMA = vol.Schema(
    {
        vol.Required(CONF_TARGET): cv.TARGET_FIELDS,
        vol.Optional(CONF_OPTIONS, default={}): {
            vol.Optional(CONF_TAG_ID): cv.string,
        },
    }
)


class _NFCTrigger(Trigger):
    """Base class for USB NFC Reader integration triggers."""

    event_activity_type: str

    @classmethod
    async def async_validate_config(
        cls,
        hass: HomeAssistant,
        config: ConfigType,
    ) -> ConfigType:
        """Validate trigger-specific configuration."""
        return cast(ConfigType, _CONFIG_SCHEMA(config))

    def __init__(self, hass: HomeAssistant, config: TriggerConfig) -> None:
        """Initialize the trigger."""
        super().__init__(hass, config)
        self._target = config.target or {}
        self._options = config.options or {}

    async def async_attach_runner(
        self,
        run_action: TriggerActionRunner,
    ) -> CALLBACK_TYPE:
        """Attach the Home Assistant event listener."""
        target_device_ids = self._target.get("device_id", [])
        if isinstance(target_device_ids, str):
            target_device_ids = [target_device_ids]
        target_device_ids = set(target_device_ids)

        selected_tag = self._options.get(CONF_TAG_ID)
        if selected_tag:
            selected_tag = str(selected_tag).upper()

        @callback
        def handle_event(event: Event) -> None:
            event_data = event.data

            if event_data.get("type") != self.event_activity_type:
                return

            if (
                target_device_ids
                and event_data.get("device_id") not in target_device_ids
            ):
                return

            uid = str(event_data.get("uid", "")).upper()
            if selected_tag and uid != selected_tag:
                return

            payload: dict[str, Any] = {
                "event": event,
                "device_id": event_data.get("device_id"),
                "uid": uid,
                "reader": event_data.get("reader"),
                "type": event_data.get("type"),
            }
            description = (
                f"USB NFC Reader {self.event_activity_type.replace('_', ' ')}"
                + (f" for tag {uid}" if uid else "")
            )
            run_action(payload, description)

        return self.hass.bus.async_listen(EVENT_DEVICE_ACTIVITY, handle_event)


class CardScannedTrigger(_NFCTrigger):
    """Trigger when an NFC card is scanned."""

    event_activity_type = "card_scanned"


class CardRemovedTrigger(_NFCTrigger):
    """Trigger when an NFC card is removed."""

    event_activity_type = "card_removed"


async def async_get_triggers(
    hass: HomeAssistant,
) -> dict[str, type[Trigger]]:
    """Return triggers provided by USB NFC Reader."""
    return {
        "card_scanned": CardScannedTrigger,
        "card_removed": CardRemovedTrigger,
    }
