from langchain.agents import create_agent
from langchain.tools import tool
from langchain_google_genai import ChatGoogleGenerativeAI

from models.health_models import HealthInsightsResponse
from models.langchain_models import ContextData

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

@tool
def get_today_health_data():
  """Fetch the user's health data for today."""
  pass

@tool 
def get_today_schedule():
  """Fetch the user's schedule for today."""
  pass

@tool
def write_to_calendar(event_details: str):
  """Write an event to the user's calendar."""
  pass

llm_model = ChatGoogleGenerativeAI(model="gemini-2.5-flash")
agent = create_agent(model=llm_model, tools=[get_users_objectives, get_today_health_data, get_today_schedule, write_to_calendar]
                     , system_prompt=SYSTEM_PROMPT, )



def create_ai_insights(user_id: str) -> HealthInsightsResponse:
  """Generate AI insights based on the user's health data and objectives."""
  response = agent.invoke({"messages": [{"role": "user", "content": "Generate personalized health insights for me based on their objectives, today's health data, and schedule."}]}, 
                          context=ContextData(user_id=user_id))

  return response

  

