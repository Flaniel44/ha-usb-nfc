from homeassistant.components.event import EventEntity
from homeassistant.helpers.dispatcher import async_dispatcher_connect

from .const import DEVICE_IDENTIFIER, DOMAIN, SIGNAL_UPDATE
from .entity import ACR122UEntity


async def async_setup_entry(hass, entry, async_add_entities):
    async_add_entities([ACR122UCardActivityEvent(entry.entry_id)])


class ACR122UCardActivityEvent(ACR122UEntity, EventEntity):
    _attr_name = "Card activity"
    _attr_unique_id = "acr122u_card_activity"
    _attr_icon = "mdi:nfc-variant"
    _attr_event_types = ["scanned", "removed"]

    async def async_added_to_hass(self) -> None:
        # Register our own dispatcher listener because event entities must
        # trigger events instead of simply writing state on every update.
        self.async_on_remove(
            async_dispatcher_connect(
                self.hass,
                SIGNAL_UPDATE,
                self._handle_reader_update,
            )
        )

    def _handle_reader_update(self, entry_id: str) -> None:
        if entry_id != self._entry_id:
            return

        state = self.reader_state
        event_type = state.get("last_event_type")
        uid = state.get("current_uid") or state.get("last_uid")

        if event_type not in self._attr_event_types or not uid:
            return

        self._trigger_event(event_type, {"uid": uid, "reader": "ACR122U"})
        self.async_write_ha_state()
