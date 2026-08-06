from homeassistant.components.binary_sensor import BinarySensorEntity, BinarySensorDeviceClass

from .entity import ACR122UEntity


async def async_setup_entry(hass, entry, async_add_entities):
    async_add_entities([ACR122UCardPresentBinarySensor(entry.entry_id)])


class ACR122UCardPresentBinarySensor(ACR122UEntity, BinarySensorEntity):
    _attr_name = "Card present"
    _attr_unique_id = "acr122u_card_present"
    _attr_device_class = BinarySensorDeviceClass.OCCUPANCY

    @property
    def is_on(self):
        return self.reader_state["present"]

    @property
    def extra_state_attributes(self):
        return {"uid": self.reader_state["current_uid"]}
