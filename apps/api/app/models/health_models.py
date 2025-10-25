from pydantic import BaseModel

class HealthData(BaseModel):
  sleep_hours: float
  sleep_score: int
  steps_count: int
  heart_rate: int
  stress_level: int

class HealthInsightsResponse(BaseModel):
  ai_insights: str = None

class HeathSuggestionsResponse(BaseModel):
  suggestions: list[str] = []

class HealthOverviewResponse(BaseModel):
  sleep_hours: float
  sleep_score: int
  steps_count: int
  heart_rate: int
  emotional_wellbeing_state: str
  ai_insights: str = None