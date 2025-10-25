from langchain.agents import create_agent
from langchain.tools import tool
from langchain_google_genai import ChatGoogleGenerativeAI
import os

from models.health_models import HealthInsightsResponse
from models.langchain_models import ContextData
from utils.random_health_data import generate_mock_health_data

SYSTEM_PROMPT = """You are a health AI assistant. 
Your goal is to help users achieve their health objectives by analyzing their daily health data and schedule. 
Use the provided tools to fetch the user's health objectives, today's health data, and today's schedule. 
Based on this information, generate personalized insights and recommendations to help the user improve their health and productivity. 
If necessary, you can also write events to the user's calendar to help them stay on track with their health goals.
"""


@tool
def get_users_objectives():
    """Fetch the user's health objectives."""
    pass


# @tool
def get_today_health_data():
    """Fetch the user's health data for today."""
    mock_data = generate_mock_health_data("realistic")

    return {
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
    }


@tool
def get_today_schedule():
    """Fetch the user's schedule for today."""
    pass


@tool
def write_to_calendar(event_details: str):
    """Write an event to the user's calendar."""
    pass


def get_llm_model():
    """Build LLM"""
    google_api_key = os.getenv("GOOGLE_API_KEY")
    if not google_api_key:
        print("⚠️ GOOGLE_API_KEY not found in environment variables")
        return None

    return ChatGoogleGenerativeAI(
        model="gemini-2.5-flash", google_api_key=google_api_key
    )


def get_agent():
    llm_model = get_llm_model()
    if not llm_model:
        return None

    return create_agent(
        model=llm_model,
        tools=[
            get_users_objectives,
            get_today_health_data,
            get_today_schedule,
            write_to_calendar,
        ],
        system_prompt=SYSTEM_PROMPT,
    )


# Lazy initialization
agent = None


def create_ai_insights(user_id: str) -> HealthInsightsResponse:
    """Generate AI insights based on the user's health data and objectives."""
    global agent

    if agent is None:
        agent = get_agent()

    if agent is None:
        return HealthInsightsResponse(
            insights="AI insights not available. Please configure GOOGLE_API_KEY.",
            recommendations=["Configure Google API key for AI insights"],
            health_score=75,
        )

    try:
        response = agent.invoke(
            {
                "messages": [
                    {
                        "role": "user",
                        "content": "Generate personalized health insights for me based on their objectives, today's health data, and schedule.",
                    }
                ]
            },
            context=ContextData(user_id=user_id),
        )

        return response
    except Exception as e:
        print(f"Error generating AI insights: {e}")
        return HealthInsightsResponse(
            insights="AI insights temporarily unavailable.",
            recommendations=["Try again later or check API configuration"],
            health_score=75,
        )
