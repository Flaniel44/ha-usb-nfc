"""Device automation triggers for the USB NFC reader."""

from __future__ import annotations

from typing import Any

import voluptuous as vol

from homeassistant.components.device_automation import DEVICE_TRIGGER_BASE_SCHEMA
from homeassistant.components.homeassistant.triggers import event as event_trigger
from homeassistant.const import (
    CONF_DEVICE_ID,
    CONF_DOMAIN,
    CONF_PLATFORM,
    CONF_TYPE,
)
from homeassistant.core import CALLBACK_TYPE, HomeAssistant
from homeassistant.helpers import config_validation as cv, selector
from homeassistant.helpers.trigger import TriggerActionType, TriggerInfo
from homeassistant.helpers.typing import ConfigType

from .const import DOMAIN, EVENT_DEVICE_ACTIVITY

CONF_TAG_ID = "tag_id"

TRIGGER_CARD_SCANNED = "card_scanned"
TRIGGER_CARD_REMOVED = "card_removed"
TRIGGER_TYPES = {TRIGGER_CARD_SCANNED, TRIGGER_CARD_REMOVED}

# Home Assistant Core applies this schema automatically.
TRIGGER_SCHEMA = DEVICE_TRIGGER_BASE_SCHEMA.extend(
    {
        vol.Required(CONF_TYPE): vol.In(TRIGGER_TYPES),
        vol.Optional(CONF_TAG_ID): cv.string,
    }
)


async def async_get_triggers(
    hass: HomeAssistant,
    device_id: str,
) -> list[dict[str, Any]]:
    """Return NFC triggers exposed for this reader device."""
    return [
        {
            CONF_PLATFORM: "device",
            CONF_DOMAIN: DOMAIN,
            CONF_DEVICE_ID: device_id,
            CONF_TYPE: trigger_type,
        }
        for trigger_type in (
            TRIGGER_CARD_SCANNED,
            TRIGGER_CARD_REMOVED,
        )
    ]


async def async_get_trigger_capabilities(
    hass: HomeAssistant,
    config: ConfigType,
) -> dict[str, vol.Schema]:
    """Return optional trigger fields shown in the automation editor."""
    return {
        "extra_fields": vol.Schema(
            {
                vol.Optional(CONF_TAG_ID): selector.TagSelector(),
            }
        )
    }


async def async_attach_trigger(
    hass: HomeAssistant,
    config: ConfigType,
    action: TriggerActionType,
    trigger_info: TriggerInfo,
) -> CALLBACK_TYPE:
    """Attach the native device trigger to the reader activity event."""
    event_data = {
        CONF_DEVICE_ID: config[CONF_DEVICE_ID],
        CONF_TYPE: config[CONF_TYPE],
    }

    if tag_id := config.get(CONF_TAG_ID):
        event_data["uid"] = tag_id.upper()

    # Validate the delegated event trigger with Home Assistant's event schema.
    event_config = event_trigger.TRIGGER_SCHEMA(
        {
            event_trigger.CONF_PLATFORM: "event",
            event_trigger.CONF_EVENT_TYPE: EVENT_DEVICE_ACTIVITY,
            event_trigger.CONF_EVENT_DATA: event_data,
        }
    )

    return await event_trigger.async_attach_trigger(
        hass,
        event_config,
        action,
        trigger_info,
        platform_type="device",
    )
