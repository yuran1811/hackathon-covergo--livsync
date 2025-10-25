from typing import List, Optional, Union
from pydantic import BaseModel


class EventParticipant(BaseModel):
    name: str
    email: str


class EventResource(BaseModel):
    name: str
    email: str


class ConferencingSettings(BaseModel):
    join_before_host: bool = True
    waiting_room: bool = False
    mute_upon_entry: bool = False
    auto_recording: str = "none"


class ConferencingConfig(BaseModel):
    conf_grant_id: str
    conf_settings: dict


class Conferencing(BaseModel):
    provider: str
    autocreate: ConferencingConfig


class CreateEventRequest(BaseModel):
    title: str
    description: Optional[str] = ""
    location: Optional[str] = ""
    start_time: Optional[Union[int, float, str]] = None
    end_time: Optional[Union[int, float, str]] = None
    start_timezone: str = "America/New_York"
    end_timezone: str = "America/New_York"
    participants: Optional[List[EventParticipant]] = None
    resources: Optional[List[EventResource]] = None
    busy: bool = True
    conferencing: Optional[Conferencing] = None
    recurrence: Optional[List[str]] = None
    calendar_id: Optional[str] = None


class EventResponse(BaseModel):
    message: str
    event: dict


class EventsListResponse(BaseModel):
    events: List[dict]
    count: int


class CalendarsResponse(BaseModel):
    calendars: List[dict]