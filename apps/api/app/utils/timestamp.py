from datetime import datetime
from typing import Optional, Union

from dateutil import parser


def parse_iso_timestamp(iso_string: str) -> int:
    """
    Parse ISO 8601 timestamp string to Unix timestamp

    Args:
        iso_string: ISO 8601 format string (e.g., "2025-10-25T00:00:00+07:00")

    Returns:
        Unix timestamp (int)
    """
    try:
        dt = parser.parse(iso_string)

        unix_timestamp = int(dt.timestamp())

        return unix_timestamp

    except Exception as e:
        raise ValueError(f"Invalid ISO 8601 timestamp format: {iso_string}")


def ensure_unix_timestamp(
    value: Union[int, float, str, datetime, None],
    *,
    allow_none: bool = True,
) -> Optional[int]:
    """Normalize a timestamp-like value to a Unix timestamp (seconds).

    Args:
        value: Timestamp expressed as unix seconds, ISO8601 string, datetime, or None.
        allow_none: Whether None values are permitted and returned unchanged.

    Returns:
        Integer Unix timestamp or None when ``allow_none`` is True and ``value`` is None.

    Raises:
        ValueError: When the value cannot be interpreted as a timestamp.
    """
    if value is None:
        if allow_none:
            return None
        raise ValueError("Timestamp value cannot be None")

    if isinstance(value, datetime):
        return int(value.timestamp())

    if isinstance(value, (int, float)):
        return int(value)

    if isinstance(value, str):
        trimmed = value.strip()

        if not trimmed:
            if allow_none:
                return None
            raise ValueError("Timestamp string is empty")

        if trimmed.isdigit():
            return int(trimmed)

        return parse_iso_timestamp(trimmed)

    raise ValueError(f"Unsupported timestamp type: {type(value)!r}")
