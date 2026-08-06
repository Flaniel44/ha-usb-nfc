import voluptuous as vol

from homeassistant.components import automation
from homeassistant.components.homeassistant.triggers import event as event_trigger
from homeassistant.const import CONF_DEVICE_ID, CONF_DOMAIN, CONF_PLATFORM, CONF_TYPE
from homeassistant.core import HomeAssistant
from homeassistant.helpers import config_validation as cv, device_registry as dr

from .const import DOMAIN, EVENT_CARD_PRESENT, EVENT_CARD_REMOVED

TRIGGER_TYPES = {"card_placed", "card_removed"}

TRIGGER_SCHEMA = vol.Schema(
    {
        vol.Required(CONF_PLATFORM): "device",
        vol.Required(CONF_DOMAIN): DOMAIN,
        vol.Required(CONF_DEVICE_ID): str,
        vol.Required(CONF_TYPE): vol.In(TRIGGER_TYPES),
    }
)


async def async_get_triggers(hass: HomeAssistant, device_id: str):
    return [
        {
            CONF_PLATFORM: "device",
            CONF_DOMAIN: DOMAIN,
            CONF_DEVICE_ID: device_id,
            CONF_TYPE: trigger_type,
        }
        for trigger_type in TRIGGER_TYPES
    ]


async def async_attach_trigger(hass, config, action, trigger_info):
    config = TRIGGER_SCHEMA(config)
    event_type = (
        EVENT_CARD_PRESENT
        if config[CONF_TYPE] == "card_placed"
        else EVENT_CARD_REMOVED
    )
    event_config = {
        event_trigger.CONF_PLATFORM: "event",
        event_trigger.CONF_EVENT_TYPE: event_type,
    }
    return await event_trigger.async_attach_trigger(
        hass,
        event_config,
        action,
        trigger_info,
        platform_type="device",
    )
