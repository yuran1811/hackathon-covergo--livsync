import os
from datetime import datetime

from dotenv import load_dotenv
from nylas import Client
from typing import Optional, Union

from app.utils.timestamp import ensure_unix_timestamp, parse_iso_timestamp


load_dotenv()


def getCalendarEvents(
    timestamp_start: int | None = None,
    timestamp_end: int | None = None,
    limit: int = 100,
):
    """
    Get calendar events with optional time filtering

    Args:
        timestamp_start: Unix timestamp for start time filter
        timestamp_end: Unix timestamp for end time filter
        calendar_id: Specific calendar ID (uses env var if not provided)
        limit: Maximum number of events to return

    Returns:
        List of events or calendars if no time filters
    """
    try:
        nylas = Client(os.environ.get("NYLAS_API_KEY") or "")
        grant_id = os.environ.get("NYLAS_GRANT_ID")

        target_calendar_id = os.environ.get("CALENDAR_ID")
        if not grant_id:
            raise Exception("NYLAS_GRANT_ID not set in environment variables")

        # Prepare query parameters
        query_params = {"calendar_id": target_calendar_id, "limit": limit}

        # Add time filters if provided
        if timestamp_start:
            query_params["start"] = timestamp_start
        if timestamp_end:
            query_params["end"] = timestamp_end

        print(f"Getting events with filters: {query_params}")

        # Get events with filters
        events = nylas.events.list(grant_id, query_params=query_params)

        print(f"Retrieved {len(events.data)} events")
        return events.data

    except Exception as e:
        print(f"Error getting calendar events: {e}")
        raise e


def getTodayEvents():
    """
    Get today's events from a calendar (from 00:00 to 23:59)
    """
    try:
        # Get current time
        now = datetime.now()
        # Get start of today (00:00:00)
        start_of_today = datetime(now.year, now.month, now.day, 0, 0, 0)

        # Get end of today (23:59:59)
        end_of_today = datetime(now.year, now.month, now.day, 23, 59, 59)

        # Convert to Unix timestamps
        start = parse_iso_timestamp(start_of_today.isoformat())
        end = parse_iso_timestamp(end_of_today.isoformat())

        events = getCalendarEvents(timestamp_start=start, timestamp_end=end)

        return events

    except Exception as e:
        print(f"Error getting today's events: {e}")
        raise e


def createCalendarEvent(
    title: str,
    description: str = "",
    location: str = "",
    start_time: Union[int, float, str, None] = None,
    end_time: Union[int, float, str, None] = None,
    start_timezone: str = "Asia/Ho_Chi_Minh",
    end_timezone: str = "Asia/Ho_Chi_Minh",
    participants: Optional[list] = None,
    resources: Optional[list] = None,
    busy: bool = True,
    conferencing: Optional[dict] = None,
    recurrence: Optional[list] = None,
    calendar_id: Optional[str] = None,
):
    """
    Create a calendar event using Nylas API

    Args:
        title: Event title
        description: Event description
        location: Event location
        start_time: Unix timestamp for start time
        end_time: Unix timestamp for end time
        start_timezone: Start timezone
        end_timezone: End timezone
        participants: List of participants with name and email
        resources: List of resources with name and email
        busy: Whether the event is busy (default: True)
        conferencing: Conferencing settings
        recurrence: List of recurrence rules
        calendar_id: Calendar ID (uses env var if not provided)

    Returns:
        Created event data or error
    """
    try:
        nylas = Client(os.environ.get("NYLAS_API_KEY") or "")
        grant_id = os.environ.get("NYLAS_GRANT_ID")

        if not grant_id:
            raise Exception("NYLAS_GRANT_ID not set in environment variables")

        # Use provided calendar_id or get from environment
        target_calendar_id = calendar_id or os.environ.get("CALENDAR_ID")
        if not target_calendar_id:
            raise Exception(
                "Calendar ID not provided and CALENDAR_ID not set in environment variables"
            )

        # Normalize timestamps if provided so downstream calls receive integers
        start_ts = ensure_unix_timestamp(start_time)
        end_ts = ensure_unix_timestamp(end_time)

        # Prepare event data
        event_data = {
            "title": title,
            "busy": busy,
            "description": description,
            "location": location,
        }

        # Add time information if provided
        if start_ts and end_ts:
            event_data["when"] = {
                "start_time": start_ts,
                "end_time": end_ts,
                "start_timezone": start_timezone,
                "end_timezone": end_timezone,
            }

        # Add participants if provided
        if participants:
            event_data["participants"] = participants

        # Add resources if provided
        if resources:
            event_data["resources"] = resources

        # Add conferencing if provided
        if conferencing:
            event_data["conferencing"] = conferencing

        # Add recurrence if provided
        if recurrence:
            event_data["recurrence"] = recurrence

        print(f"Creating event with data: {event_data}")

        # Create the event
        event = nylas.events.create(
            grant_id,
            request_body=event_data,
            query_params={"calendar_id": target_calendar_id},
        )

        print(f"Event created successfully: {event}")
        return event

    except Exception as e:
        print(f"Error creating calendar event: {e}")
        raise e


def createSampleEvent():
    """
    Create a sample event based on the provided curl request
    """
    sample_event = createCalendarEvent(
        title="Annual Philosophy Club Meeting",
        description="Come ready to talk philosophy!",
        location="New York Public Library, Cave room",
        start_time=1674604800,
        end_time=1722382420,
        start_timezone="America/New_York",
        end_timezone="America/New_York",
        participants=[
            {"name": "Leyah Miller", "email": "leyah@example.com"},
            {"name": "Nyla", "email": "nyla@example.com"},
        ],
        resources=[{"name": "Conference room", "email": "conference-room@example.com"}],
        busy=True,
        conferencing={
            "provider": "Zoom Meeting",
            "autocreate": {
                "conf_grant_id": os.environ.get("NYLAS_GRANT_ID"),
                "conf_settings": {
                    "settings": {
                        "join_before_host": True,
                        "waiting_room": False,
                        "mute_upon_entry": False,
                        "auto_recording": "none",
                    }
                },
            },
        },
        recurrence=["RRULE:FREQ=WEEKLY;BYDAY=MO", "EXDATE:20211011T000000Z"],
    )

    return sample_event


def getAllEvents(calendar_id: str | None = None, limit: int = 100):
    """
    Get all events from a calendar

    Args:
        calendar_id: Calendar ID (uses env var if not provided)
        limit: Maximum number of events to return

    Returns:
        List of events
    """
    try:
        nylas = Client(os.environ.get("NYLAS_API_KEY") or "")
        grant_id = os.environ.get("NYLAS_GRANT_ID")

        if not grant_id:
            raise Exception("NYLAS_GRANT_ID not set in environment variables")

        # Use provided calendar_id or get from environment
        target_calendar_id = calendar_id or os.environ.get("CALENDAR_ID")
        if not target_calendar_id:
            raise Exception(
                "Calendar ID not provided and CALENDAR_ID not set in environment variables"
            )

        # Get events
        events = nylas.events.list(
            grant_id=grant_id,
            query_params={"calendar_id": target_calendar_id, "limit": limit},
        )

        print(f"Retrieved {len(events.data)} events")
        return events.data

    except Exception as e:
        print(f"Error getting events: {e}")
        raise e
