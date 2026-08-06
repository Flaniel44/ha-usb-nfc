from __future__ import annotations

from homeassistant.components.tag import async_scan_tag
from homeassistant.config_entries import ConfigEntry
from homeassistant.core import Event, HomeAssistant, callback
from homeassistant.helpers import device_registry as dr
from homeassistant.helpers.dispatcher import async_dispatcher_send

from .const import (
    DEVICE_IDENTIFIER,
    DOMAIN,
    EVENT_CARD_PRESENT,
    EVENT_CARD_REMOVED,
    PLATFORMS,
    SIGNAL_UPDATE,
)


async def async_setup_entry(hass: HomeAssistant, entry: ConfigEntry) -> bool:
    hass.data.setdefault(DOMAIN, {})
    hass.data[DOMAIN][entry.entry_id] = {
        "present": False,
        "current_uid": None,
        "last_uid": None,
        "last_event_type": None,
    }

    device_registry = dr.async_get(hass)
    device = device_registry.async_get_or_create(
        config_entry_id=entry.entry_id,
        identifiers={(DOMAIN, DEVICE_IDENTIFIER)},
        manufacturer="Advanced Card Systems",
        model="ACR122U",
        name="USB NFC Reader",
    )

    @callback
    def handle_present(event: Event) -> None:
        uid = str(event.data.get("uid", "")).upper()
        if not uid:
            return

        state = hass.data[DOMAIN][entry.entry_id]
        state["present"] = True
        state["current_uid"] = uid
        state["last_uid"] = uid
        state["last_event_type"] = "scanned"
        async_dispatcher_send(hass, SIGNAL_UPDATE, entry.entry_id)

        hass.async_create_task(
            async_scan_tag(hass, uid, device.id, context=event.context)
        )

    @callback
    def handle_removed(event: Event) -> None:
        state = hass.data[DOMAIN][entry.entry_id]
        state["present"] = False
        state["current_uid"] = None
        state["last_event_type"] = "removed"
        async_dispatcher_send(hass, SIGNAL_UPDATE, entry.entry_id)

    unsub_present = hass.bus.async_listen(EVENT_CARD_PRESENT, handle_present)
    unsub_removed = hass.bus.async_listen(EVENT_CARD_REMOVED, handle_removed)
    entry.async_on_unload(unsub_present)
    entry.async_on_unload(unsub_removed)

    await hass.config_entries.async_forward_entry_setups(entry, PLATFORMS)
    return True


async def async_unload_entry(hass: HomeAssistant, entry: ConfigEntry) -> bool:
    unloaded = await hass.config_entries.async_unload_platforms(entry, PLATFORMS)
    if unloaded:
        hass.data[DOMAIN].pop(entry.entry_id, None)
    return unloaded
