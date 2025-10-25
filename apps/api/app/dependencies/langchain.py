from typing import Any

from langchain.agents import create_agent
from langchain.tools import tool
from langchain_google_genai import ChatGoogleGenerativeAI

from app.models.health_models import HealthInsightsResponse

from .config import GEMINI_API_KEY
from .supabase import supabase_client

SYSTEM_PROMPT = """You are a health AI assistant. 
Your goal is to help users achieve their health objectives by analyzing their daily health data and schedule. 
Use the provided tools to fetch the user's health objectives, today's health data, and today's schedule. 
Based on this information, generate personalized insights and recommendations to help the user improve their health and productivity. 
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

@tool
def get_today_health_data():
  """Fetch the user's health data for today."""
  return "User's health data for today: 8000 steps taken, 7 hours of sleep, 2000 calories consumed."

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
