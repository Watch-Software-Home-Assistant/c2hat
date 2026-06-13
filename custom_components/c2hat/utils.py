"""Utils for the C2hat integration."""

import logging

import aiofiles
from slack_sdk.errors import SlackApiError
from slack_sdk.web.async_client import AsyncWebClient

_LOGGER = logging.getLogger(__name__)


async def upload_file_to_c2hat(
    client: AsyncWebClient,
    channel_ids: list[str | None],
    file_content: bytes | str | None,
    filename: str,
    title: str | None,
    message: str,
    thread_ts: str | None,
    file_path: str | None = None,
) -> None:
    """Upload a file to C2hat for the specified channel IDs."""
    if file_content is None and file_path:
        try:
            async with aiofiles.open(file_path, "rb") as file:
                file_content = await file.read()
        except OSError as os_err:
            _LOGGER.error("Error reading file %s: %r", file_path, os_err)
            return

    for channel_id in channel_ids:
        try:
            await client.files_upload_v2(
                channel=channel_id,
                file=file_content,
                filename=filename,
                title=title or filename,
                initial_comment=message,
                thread_ts=thread_ts or "",
            )
            _LOGGER.info("Successfully uploaded file to channel %s", channel_id)
        except SlackApiError as err:
            _LOGGER.error(
                "Error while uploading file to channel %s: %r", channel_id, err
            )
