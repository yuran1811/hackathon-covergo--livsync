import json
from dataclasses import dataclass
from datetime import datetime
from typing import Any
from zoneinfo import ZoneInfo

from langchain.agents import create_agent
from langchain.tools import tool
from langchain_google_genai import ChatGoogleGenerativeAI

from app.dependencies.calendar import getTodayEvents
from app.dependencies.supabase import supabase_client
from app.models.health_models import HealthInsightsResponse
from app.utils.random_health_data import get_persisted_mock_health_data

SYSTEM_PROMPT = """You are a health AI assistant.
Your goal is to help users achieve their health objectives by analyzing their daily health data and schedule. 
Use the provided tools to fetch the user's health objectives, today's health data, and today's schedule. 
Based on this information, help users with their requests.
Just tell meaningful insights based on the data provided. Don't just repeat the data back to the user.
Healthy sleep range: 7-9 hours per night.
Good sleep quality: above 80.
Stress level: below 50 is considered low stress.
"""


@dataclass
class EventSuggestion:
    """Structured response for calendar suggestions."""

    start_time: str
    end_time: str
    title: str
    description: str
    rationale: str


EVENT_SUGGESTION_PROMPT = """You are a health-focused scheduling assistant.
Recommend calendar adjustments that keep the user on track with health goals.
When proposing an event, ensure the times are in ISO 8601 format and the plan is concise."""


@tool
def get_users_objectives(user_id: str):
    """Fetch the user's health objectives."""
    try:
        res = supabase_client.table("users").select("*").eq("id", user_id).execute()
        if len(res.data) == 0:
            return "User not found."

        user_data: Any = res.data[0]
        return f"My step goal is {user_data['step_goal']} steps per day. My custom goals are: {user_data['custom_goals']}"
    except Exception as e:
        return f"An error occurred while fetching user objectives: {str(e)}"


@tool
def get_today_health_data():
    """Fetch the user's health data for today."""
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


@tool
def get_today_schedule():
    """Fetch the user's schedule for today."""
    res = getTodayEvents()
    events = [
        f"{datetime.fromtimestamp(_.when.start_time).strftime('%H:%M:%S')} - {
            _.title
        } ({_.description})"
        for _ in res
    ]
    return "User's schedule for today: " + ", ".join(events)

llm_model = ChatGoogleGenerativeAI(model="gemini-2.5-flash")
agent = create_agent(
    model=llm_model,
    tools=[
        get_users_objectives,
        get_today_health_data,
        get_today_schedule,
    ],
    system_prompt=SYSTEM_PROMPT,
)


event_suggestion_agent = create_agent(
    model=llm_model,
    tools=[
        get_users_objectives,
        get_today_health_data,
        get_today_schedule,
    ],
    system_prompt=EVENT_SUGGESTION_PROMPT,
    response_format=EventSuggestion,
)


def adapt_event_changes(event_list: list[str]):
    pass


def create_ai_insights(user_id: str) -> HealthInsightsResponse | Any:
    """Generate AI insights based on the user's health data and objectives."""
    current_datetime = datetime.now()

    response = agent.invoke(
        {
            "messages": [
                {
                    "role": "user",
                    "content": f"Generate personalized health insights for me based on their objectives, today's health data, and schedule. My user ID is {user_id}. Current date and time is {current_datetime.strftime('%Y-%m-%d %H:%M:%S')}.",
                }
            ]
        },
    )

    return (
        "\n".join(
            [_["text"] for _ in response["messages"][-1].content if _["type"] == "text"]
        )
        or "No insights generated."
    )


def ai_event_changed_suggestions(user_id: str, changed_events: list[str]) -> Any:
    """Generate AI suggestions for adapting to changed events in the user's schedule."""
    if not changed_events:
        return "No changed events provided."

    response = event_suggestion_agent.invoke(
        {
            "messages": [
                {
                    "role": "user",
                    "content": (
                        f"My user ID is {user_id}. Given these schedule changes: {', '.join(changed_events)}, suggest a replacement event in ISO 8601 format that keeps me aligned with my health goals. "
                        "If nothing needs to change, simply respond with 'No changes needed.'"
                    ),
                }
            ]
        }
    )

    structured = response.get("structured_response")
    if structured:
        return structured

    return (
        "\n".join(
            [_["text"] for _ in response["messages"][-1].content if _["type"] == "text"]
        )
        or "No suggestions generated."
    )


def ai_event_day_suggestions(user_id: str) -> Any:
    """Generate AI suggestions for a specific day based on events in the user's schedule."""
    current_datetime = datetime.now()
    response = event_suggestion_agent.invoke(
        {
            "messages": [
                {
                    "role": "user",
                    "content": (
                        f"My user ID is {user_id}. Review today's health objectives, custom goals and calendar, then propose one supportive event in ISO 8601 format. Current date and time is {current_datetime.strftime('%Y-%m-%d %H:%M:%S')}"
                        "If no change is required, respond with 'No changes needed.'"
                    ),
                }
            ]
        }
    )

    structured = response.get("structured_response")
    if structured:
        return structured

    return (
        "\n".join(
            [_["text"] for _ in response["messages"][-1].content if _["type"] == "text"]
        )
        or "No suggestions generated."
    )


def generate_structured_event_suggestion(user_id: str) -> EventSuggestion | str:
    """Generate a structured event suggestion to reinforce health goals."""
    response = event_suggestion_agent.invoke(
        {
            "messages": [
                {
                    "role": "user",
                    "content": (
                        f"My user ID is {user_id}. Review my health targets, and current schedule, then propose a single event that helps me stay aligned with my goals."
                    ),
                }
            ]
        }
    )

    structured = response.get("structured_response")
    return structured if structured else "No suggestion generated."