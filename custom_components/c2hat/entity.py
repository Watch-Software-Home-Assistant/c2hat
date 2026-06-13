"""The C2hat integration."""

from homeassistant.helpers.device_registry import DeviceEntryType, DeviceInfo
from homeassistant.helpers.entity import Entity, EntityDescription

from . import C2hatConfigEntry, C2hatData
from .const import DEFAULT_NAME, DOMAIN


class C2hatEntity(Entity):
    """Representation of a C2hat entity."""

    def __init__(
        self,
        data: C2hatData,
        description: EntityDescription,
        entry: C2hatConfigEntry,
    ) -> None:
        """Initialize a C2hat entity."""
        self._client = data.client
        self.entity_description = description
        self._attr_unique_id = f"{data.user_id}_{description.key}"
        self._attr_device_info = DeviceInfo(
            configuration_url=data.url,
            entry_type=DeviceEntryType.SERVICE,
            identifiers={(DOMAIN, entry.entry_id)},
            manufacturer=DEFAULT_NAME,
            name=entry.title,
        )
