from homeassistant.components.sensor import SensorEntity

from .entity import ACR122UEntity


async def async_setup_entry(hass, entry, async_add_entities):
    async_add_entities([
        ACR122UCurrentTagSensor(entry.entry_id),
        ACR122ULastTagSensor(entry.entry_id),
    ])


class ACR122UCurrentTagSensor(ACR122UEntity, SensorEntity):
    _attr_name = "Current tag"
    _attr_unique_id = "acr122u_current_tag"
    _attr_icon = "mdi:nfc"

    @property
    def native_value(self):
        return self.reader_state["current_uid"]


class ACR122ULastTagSensor(ACR122UEntity, SensorEntity):
    _attr_name = "Last tag"
    _attr_unique_id = "acr122u_last_tag"
    _attr_icon = "mdi:nfc-variant"

    @property
    def native_value(self):
        return self.reader_state["last_uid"]
