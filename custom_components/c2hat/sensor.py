"""C2hat platform for sensor component."""

from slack_sdk.web.async_client import AsyncWebClient

from homeassistant.components.sensor import (
    SensorDeviceClass,
    SensorEntity,
    SensorEntityDescription,
)
from homeassistant.core import HomeAssistant
from homeassistant.helpers.entity_platform import AddConfigEntryEntitiesCallback
from homeassistant.util import dt as dt_util

from . import C2hatConfigEntry
from .const import ATTR_SNOOZE
from .entity import C2hatEntity


async def async_setup_entry(
    hass: HomeAssistant,
    entry: C2hatConfigEntry,
    async_add_entities: AddConfigEntryEntitiesCallback,
) -> None:
    """Set up the C2hat sensor."""
    async_add_entities(
        [
            C2hatSensorEntity(
                entry.runtime_data,
                SensorEntityDescription(
                    key="do_not_disturb_until",
                    translation_key="do_not_disturb_until",
                    device_class=SensorDeviceClass.TIMESTAMP,
                ),
                entry,
            )
        ],
        True,
    )


class C2hatSensorEntity(C2hatEntity, SensorEntity):
    """Representation of a C2hat sensor."""

    _client: AsyncWebClient

    async def async_update(self) -> None:
        """Get the latest status."""
        if _time := (await self._client.dnd_info()).get(ATTR_SNOOZE):
            self._attr_native_value = dt_util.utc_from_timestamp(_time)
        else:
            self._attr_native_value = None
