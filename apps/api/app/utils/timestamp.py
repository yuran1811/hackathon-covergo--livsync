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

    except Exception:
        raise ValueError(f"Invalid ISO 8601 timestamp format: {iso_string}")


def ensure_unix_timestamp(timestamp: int | float | str | None) -> int:
    """
    Ensure the input is a Unix timestamp. If it's a string, parse it as ISO 8601.

    Args:
        timestamp: Unix timestamp (int) or ISO 8601 string

    Returns:
        Unix timestamp (int)
    """
    if isinstance(timestamp, int):
        return timestamp
    elif isinstance(timestamp, str):
        return parse_iso_timestamp(timestamp)
    else:
        raise TypeError("Timestamp must be an integer or ISO 8601 string")
