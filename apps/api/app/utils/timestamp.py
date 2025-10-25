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
