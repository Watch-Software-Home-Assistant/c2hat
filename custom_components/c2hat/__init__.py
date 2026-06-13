"""The C2hat integration."""

from dataclasses import dataclass
import logging

from aiohttp.client_exceptions import ClientError
from slack_sdk.errors import SlackApiError
from slack_sdk.web.async_client import AsyncWebClient

from homeassistant.config_entries import ConfigEntry
from homeassistant.const import CONF_API_KEY, Platform
from homeassistant.core import HomeAssistant
from homeassistant.exceptions import ConfigEntryNotReady
from homeassistant.helpers import aiohttp_client, config_validation as cv, discovery
from homeassistant.helpers.typing import ConfigType

from .const import (
    ATTR_URL,
    ATTR_USER_ID,
    C2HAT_DATA,
    CONF_BASE_URL,
    DATA_CLIENT,
    DATA_HASS_CONFIG,
    DEFAULT_BASE_URL,
    DOMAIN,
)

_LOGGER = logging.getLogger(__name__)

PLATFORMS = [Platform.NOTIFY, Platform.SENSOR]

CONFIG_SCHEMA = cv.config_entry_only_config_schema(DOMAIN)

type C2hatConfigEntry = ConfigEntry[C2hatData]


@dataclass
class C2hatData:
    """Runtime data for the C2hat integration."""

    client: AsyncWebClient
    url: str
    user_id: str


async def async_setup(hass: HomeAssistant, config: ConfigType) -> bool:
    """Set up the C2hat component."""
    hass.data[DATA_HASS_CONFIG] = config
    return True


async def async_setup_entry(hass: HomeAssistant, entry: C2hatConfigEntry) -> bool:
    """Set up C2hat from a config entry."""
    session = aiohttp_client.async_get_clientsession(hass)
    # base_url override is what redirects the slack_sdk client at c2hat's
    # Slack-API-compatible endpoint instead of slack.com. The rest of the
    # SDK calls (chat_postMessage, files_upload, auth_test, etc.) work
    # unchanged because c2hat returns Slack-shaped response envelopes.
    base_url = entry.data.get(CONF_BASE_URL, DEFAULT_BASE_URL)
    client = AsyncWebClient(
        token=entry.data[CONF_API_KEY],
        base_url=base_url,
        session=session,
    )

    try:
        res = await client.auth_test()
    except (SlackApiError, ClientError) as ex:
        if isinstance(ex, SlackApiError) and ex.response["error"] == "invalid_auth":
            _LOGGER.error("Invalid API key")
            return False
        raise ConfigEntryNotReady("Error while setting up integration") from ex

    entry.runtime_data = C2hatData(
        client=client,
        url=res[ATTR_URL],
        user_id=res[ATTR_USER_ID],
    )

    hass.async_create_task(
        discovery.async_load_platform(
            hass,
            Platform.NOTIFY,
            DOMAIN,
            entry.data
            | {
                C2HAT_DATA: {
                    DATA_CLIENT: client,
                    ATTR_URL: res[ATTR_URL],
                    ATTR_USER_ID: res[ATTR_USER_ID],
                }
            },
            hass.data[DATA_HASS_CONFIG],
        )
    )

    await hass.config_entries.async_forward_entry_setups(
        entry, [platform for platform in PLATFORMS if platform != Platform.NOTIFY]
    )

    return True
