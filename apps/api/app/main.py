from typing import Optional

from fastapi import FastAPI, HTTPException

from app.dependencies.calendar import (
    createCalendarEvent,
    createSampleEvent,
    getCalendarEvents,
    getTodayEvents,
)
from app.dependencies.langchain import create_ai_insights
from app.models.calendar import CreateEventRequest
from app.utils.timestamp import parse_iso_timestamp

app = FastAPI()


@app.get("/")
def read_root():
    return {"Hello": "World", "message": "Calendar API is running"}


@app.get("/calendar/events")
async def get_all_events(
    limit: int = 100,
    timestamp_start: Optional[str] = None,
    timestamp_end: Optional[str] = None,
):
    """
    Get events from a calendar with optional time filtering

    Query Parameters:
    - limit: Maximum number of events (default: 100)
    - timestamp_start: ISO 8601 timestamp for start time filter (optional)
      Example: "2025-10-25T00:00:00+07:00"
    - timestamp_end: ISO 8601 timestamp for end time filter (optional)
      Example: "2025-10-25T23:59:00+07:00"

    If no time filters provided, returns all calendars
    """
    try:
        # Parse ISO 8601 timestamps to Unix timestamps
        unix_start = None
        unix_end = None

        if timestamp_start:
            unix_start = parse_iso_timestamp(timestamp_start)
        if timestamp_end:
            unix_end = parse_iso_timestamp(timestamp_end)

        events = getCalendarEvents(
            timestamp_start=unix_start, timestamp_end=unix_end, limit=limit
        )
        return {"events": events, "count": len(events)}
    except ValueError as e:
        raise HTTPException(
            status_code=400, detail=f"Invalid timestamp format: {str(e)}"
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error getting events: {str(e)}")


@app.get("/calendar/events/today")
async def get_today_events():
    try:
        events = getTodayEvents()
        return {"events": events, "count": len(events)}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error getting events: {str(e)}")


@app.post("/calendar/events")
async def create_event(event_data: CreateEventRequest):
    """
    Create a new calendar event. start_time and end_time may be Unix seconds or ISO 8601 strings.
    """
    try:
        # Convert Pydantic models to dictionaries
        participants = (
            [p.dict() for p in event_data.participants]
            if event_data.participants
            else None
        )
        resources = (
            [r.dict() for r in event_data.resources] if event_data.resources else None
        )
        conferencing = (
            event_data.conferencing.dict() if event_data.conferencing else None
        )

        event = createCalendarEvent(
            title=event_data.title,
            description=event_data.description,
            location=event_data.location,
            start_time=event_data.start_time,
            end_time=event_data.end_time,
            start_timezone=event_data.start_timezone,
            end_timezone=event_data.end_timezone,
            participants=participants,
            resources=resources,
            busy=event_data.busy,
            conferencing=conferencing,
            recurrence=event_data.recurrence,
            calendar_id=event_data.calendar_id,
        )

        return {"message": "Event created successfully", "event": event}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error creating event: {str(e)}")


@app.get("/users/{user_id}")
def read_user(user_id: str):
    return create_ai_insights(user_id=user_id)
