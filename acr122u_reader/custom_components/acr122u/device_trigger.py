from __future__ import annotations

from typing import Any

import voluptuous as vol

from homeassistant.components.homeassistant.triggers import event as event_trigger
from homeassistant.const import (
    CONF_DEVICE_ID,
    CONF_DOMAIN,
    CONF_PLATFORM,
    CONF_TYPE,
)
from homeassistant.core import HomeAssistant
from homeassistant.helpers import config_validation as cv, selector
from homeassistant.helpers.typing import ConfigType

from .const import DOMAIN, EVENT_CARD_PRESENT, EVENT_CARD_REMOVED

CONF_TAG_ID = "tag_id"

TRIGGER_CARD_SCANNED = "card_scanned"
TRIGGER_CARD_REMOVED = "card_removed"
TRIGGER_TYPES = {TRIGGER_CARD_SCANNED, TRIGGER_CARD_REMOVED}

TRIGGER_SCHEMA = cv.DEVICE_TRIGGER_BASE_SCHEMA.extend(
    {
        vol.Required(CONF_TYPE): vol.In(TRIGGER_TYPES),
        vol.Optional(CONF_TAG_ID): cv.string,
    }
)


async def async_get_triggers(
    hass: HomeAssistant,
    device_id: str,
) -> list[dict[str, Any]]:
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
    """Return optional fields shown after the device trigger is selected."""
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
    action,
    trigger_info,
):
    config = TRIGGER_SCHEMA(config)

    event_type = (
        EVENT_CARD_PRESENT
        if config[CONF_TYPE] == TRIGGER_CARD_SCANNED
        else EVENT_CARD_REMOVED
    )

    event_config = {
        event_trigger.CONF_PLATFORM: "event",
        event_trigger.CONF_EVENT_TYPE: event_type,
    }

    selected_tag = config.get(CONF_TAG_ID)
    if selected_tag:
        event_config[event_trigger.CONF_EVENT_DATA] = {"uid": selected_tag}

    return await event_trigger.async_attach_trigger(
        hass,
        event_config,
        action,
        trigger_info,
        platform_type="device",
    )
