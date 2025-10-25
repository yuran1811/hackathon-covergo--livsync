from typing import Any

from langchain.agents import create_agent
from langchain.tools import tool
from langchain_google_genai import ChatGoogleGenerativeAI
import os

from app.models.health_models import HealthInsightsResponse
from app.utils.random_health_data import generate_mock_health_data

from .config import GEMINI_API_KEY
from .supabase import supabase_client

SYSTEM_PROMPT = """You are a health AI assistant. 
Your goal is to help users achieve their health objectives by analyzing their daily health data and schedule. 
Use the provided tools to fetch the user's health objectives, today's health data, and today's schedule. 
Based on this information, generate personalized insights and recommendations to help the user improve their health and productivity.
Just tell meaningful insights based on the data provided. Don't just repeat the data back to the user.
If necessary, you can also write events to the user's calendar to help them stay on track with their health goals.
"""


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
  return "User's schedule for today: 9 AM - Team Meeting, 11 AM - Project Work, 2 PM - Gym, 5 PM - Dinner with Friends."


@tool
def write_to_calendar(event_details: str):
    """Write an event to the user's calendar."""
    pass

llm_model = ChatGoogleGenerativeAI(model="gemini-2.5-flash")
agent = create_agent(
  model=llm_model,
  tools=[get_users_objectives, get_today_health_data, get_today_schedule, write_to_calendar],
  system_prompt=SYSTEM_PROMPT
)

def create_ai_insights(user_id: str) -> HealthInsightsResponse | Any:
  """Generate AI insights based on the user's health data and objectives."""
  response = agent.invoke(
    {
      "messages": [
        {
          "role": "user",
          "content": f"Generate personalized health insights for me based on their objectives, today's health data, and schedule. My user ID is {user_id}"
        }
      ]
    },
  )

  return "\n".join([_["text"] for _ in response["messages"][-1].content if _["type"] == "text"]) or "No insights generated."
