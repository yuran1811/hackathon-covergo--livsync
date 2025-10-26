import datetime

from pydantic import BaseModel


class User(BaseModel):
    id: str
    email: str
    full_name: str
    custom_goals: str
    activity_level: str
    step_goal: int
    dob: datetime.date
    gender: str
    weight: int
    height: int
