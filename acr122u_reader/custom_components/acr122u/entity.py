from homeassistant.helpers.device_registry import DeviceInfo
from homeassistant.helpers.entity import Entity
from homeassistant.helpers.dispatcher import async_dispatcher_connect

from .const import DEVICE_IDENTIFIER, DOMAIN, SIGNAL_UPDATE


class ACR122UEntity(Entity):
    _attr_has_entity_name = True

    def __init__(self, entry_id: str) -> None:
        self._entry_id = entry_id
        self._attr_device_info = DeviceInfo(
            identifiers={(DOMAIN, DEVICE_IDENTIFIER)},
            manufacturer="Advanced Card Systems",
            model="ACR122U",
            name="USB NFC Reader",
        )

    async def async_added_to_hass(self) -> None:
        self.async_on_remove(
            async_dispatcher_connect(
                self.hass,
                SIGNAL_UPDATE,
                self._handle_dispatcher_update,
            )
        )

    def _handle_dispatcher_update(self, entry_id: str) -> None:
        if entry_id == self._entry_id:
            self.async_write_ha_state()

    @property
    def reader_state(self):
        return self.hass.data[DOMAIN][self._entry_id]
