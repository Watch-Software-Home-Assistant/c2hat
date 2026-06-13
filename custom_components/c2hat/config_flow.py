"""Config flow for C2hat integration."""

import logging

from slack_sdk.errors import SlackApiError
from slack_sdk.web.async_client import AsyncSlackResponse, AsyncWebClient
import voluptuous as vol

from homeassistant.config_entries import ConfigFlow, ConfigFlowResult
from homeassistant.const import CONF_API_KEY, CONF_ICON, CONF_NAME, CONF_USERNAME
from homeassistant.helpers import aiohttp_client

from .const import (
    CONF_BASE_URL,
    CONF_DEFAULT_CHANNEL,
    DEFAULT_BASE_URL,
    DOMAIN,
)

_LOGGER = logging.getLogger(__name__)

CONFIG_SCHEMA = vol.Schema(
    {
        vol.Required(CONF_API_KEY): str,
        vol.Required(CONF_DEFAULT_CHANNEL): str,
        vol.Optional(CONF_BASE_URL, default=DEFAULT_BASE_URL): str,
        vol.Optional(CONF_ICON): str,
        vol.Optional(CONF_USERNAME): str,
    }
)


class C2hatFlowHandler(ConfigFlow, domain=DOMAIN):
    """Handle a config flow for C2hat."""

    async def async_step_user(
        self, user_input: dict[str, str] | None = None
    ) -> ConfigFlowResult:
        """Handle a flow initiated by the user."""
        errors = {}

        if user_input is not None:
            error, info = await self._async_try_connect(
                user_input[CONF_API_KEY],
                user_input.get(CONF_BASE_URL, DEFAULT_BASE_URL),
            )
            if error is not None:
                errors["base"] = error
            elif info is not None:
                await self.async_set_unique_id(info["team_id"].lower())
                self._abort_if_unique_id_configured()
                return self.async_create_entry(
                    title=user_input.get(CONF_NAME, info["team"]),
                    data={CONF_NAME: user_input.get(CONF_NAME, info["team"])}
                    | user_input,
                )

        user_input = user_input or {}
        return self.async_show_form(
            step_id="user",
            data_schema=CONFIG_SCHEMA,
            errors=errors,
        )

    async def _async_try_connect(
        self, token: str, base_url: str
    ) -> tuple[str, None] | tuple[None, AsyncSlackResponse]:
        """Try connecting to C2hat."""
        session = aiohttp_client.async_get_clientsession(self.hass)
        client = AsyncWebClient(token=token, base_url=base_url, session=session)

        try:
            info = await client.auth_test()
        except SlackApiError as ex:
            if ex.response["error"] == "invalid_auth":
                return "invalid_auth", None
            return "cannot_connect", None
        except Exception:
            _LOGGER.exception("Unexpected exception")
            return "unknown", None
        return None, info
