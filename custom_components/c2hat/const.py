"""Constants for the C2hat integration."""

from typing import Final

ATTR_BLOCKS = "blocks"
ATTR_BLOCKS_TEMPLATE = "blocks_template"
ATTR_FILE = "file"
ATTR_PASSWORD = "password"
ATTR_PATH = "path"
ATTR_SNOOZE = "snooze_endtime"
ATTR_URL = "url"
ATTR_USERNAME = "username"
ATTR_USER_ID = "user_id"
ATTR_THREAD_TS = "thread_ts"

CONF_DEFAULT_CHANNEL = "default_channel"
CONF_BASE_URL = "base_url"

DATA_CLIENT = "client"
DEFAULT_NAME = "C2hat"
DEFAULT_TIMEOUT_SECONDS = 15
# Points at Tora's Slack-Web-API parity layer. The forked AsyncWebClient
# is constructed with this as base_url so every subsequent SDK call
# (chat_postMessage, auth_test, files_upload, conversations_list)
# hits the c2hat server instead of slack.com.
DEFAULT_BASE_URL: Final = "https://tora.c-2.co.uk/api/c2hat-slack/"
DOMAIN: Final = "c2hat"

C2HAT_DATA = "data"
DATA_HASS_CONFIG = "c2hat_hass_config"
