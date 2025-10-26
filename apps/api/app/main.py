import json
from contextlib import asynccontextmanager
from dataclasses import asdict, is_dataclass
from typing import Optional

from fastapi import Depends, FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

from app.dependencies.auth import get_current_user
from app.dependencies.calendar import (
    createCalendarEvent,
    getCalendarEvents,
    getTodayEvents,
)
from app.dependencies.langchain import (
    ai_event_day_suggestions,
    ai_health_chatbot_conversation,
    create_ai_insights,
)
from app.dependencies.user_profile import (
    create_user_profile,
    get_user_profile,
    update_user_profile,
)
from app.models.calendar import CreateEventRequest
from app.utils.event_poller import event_poller
from app.utils.random_health_data import get_persisted_mock_health_data
from app.utils.timestamp import parse_iso_timestamp


@asynccontextmanager
async def lifespan(app: FastAPI):
    await event_poller.start()
    yield
    await event_poller.stop()


app = FastAPI(lifespan=lifespan)

origins = [
    "http://localhost.tiangolo.com",
    "https://localhost.tiangolo.com",
    "http://localhost",
    "http://localhost:8080",
    "http://localhost:3000",
    "http://localhost:5173",
    "http://localhost:8000",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/")
def read_root():
    return {"Hello": "World", "message": "Calendar API is running"}


@app.get("/health/insights")
async def health_insights(user_id: str = Depends(get_current_user)):
    return create_ai_insights(user_id=user_id)


@app.get("health/data")
async def health_data(user_id: str = Depends(get_current_user)):
    mock_data = get_persisted_mock_health_data("realistic")

    return json.dumps(
        {
            "steps": mock_data["steps"],
            "distance_meters": mock_data["distance_meters"],
            "calories_burned": mock_data["calories_burned"],
            "sleep_duration": mock_data["sleep_duration"],
            "sleep_quality": mock_data["sleep_quality"],
            "heart_rate": mock_data["heart_rate"],
            "stress_score": mock_data["stress_score"],
            "bp_systolic": mock_data["bp_systolic"],
            "bp_diastolic": mock_data["bp_diastolic"],
            "blood_glucose": mock_data["blood_glucose"],
            "blood_oxygen": mock_data["blood_oxygen"],
            "blood_pressure": mock_data["blood_pressure"],
            "timestamp": mock_data["timestamp"],
            "weekly_workouts": mock_data["weekly_workouts"],
        }
    )


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


@app.post("/calendar/events")
async def create_event(event_data: CreateEventRequest):
    """
    Create a new calendar event. start_time and end_time may be Unix seconds or ISO 8601 strings.
    """
    try:
        # Convert Pydantic models to dictionaries
        participants = (
            [p.model_dump() for p in event_data.participants]
            if event_data.participants
            else None
        )
        resources = (
            [r.model_dump() for r in event_data.resources]
            if event_data.resources
            else None
        )
        conferencing = (
            event_data.conferencing.model_dump() if event_data.conferencing else None
        )

        event = createCalendarEvent(
            title=event_data.title,
            description=event_data.description or "",
            location=event_data.location or "",
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


@app.get("/calendar/events/today")
async def get_today_events():
    try:
        events = getTodayEvents()
        return {"events": events, "count": len(events)}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error getting events: {str(e)}")


@app.post("/users")
async def create_profile(profile_data: dict):
    return await create_user_profile(profile_data=profile_data)


@app.get("/users/{user_id}")
async def read_profile(user_id: str):
    return await get_user_profile(user_id=user_id)


@app.put("/users/{user_id}")
async def update_profile(user_id: str, profile_data: dict):
    print("Received profile data:", profile_data)
    return await update_user_profile(user_id=user_id, profile_data=profile_data)


@app.get("/users/{user_id}/insights")
async def read_user(user_id: str = Depends(get_current_user)):
    return create_ai_insights(user_id=user_id)


@app.get("/event-day-suggestion")
async def get_event_day_suggestion(user_id: str = Depends(get_current_user)):
    try:
        suggestion = ai_event_day_suggestions(user_id=user_id)

        if is_dataclass(suggestion):
            return {"suggestion": asdict(suggestion)}

        return {"suggestion": suggestion}
    except Exception as exc:
        raise HTTPException(
            status_code=500, detail=f"Error generating event suggestion: {exc}"
        )


class ChatRequest(BaseModel):
    user_message: str


@app.post("/chat/message")
async def chat_message(request: ChatRequest, user_id: str = Depends(get_current_user)):
    try:
        response = ai_health_chatbot_conversation(
            user_id=user_id,
            user_message=request.user_message,
        )

        return {"response": response}
    except Exception as exc:
        raise HTTPException(
            status_code=500, detail=f"Error generating chatbot response: {exc}"
        )
