from fastapi import APIRouter, status, Depends
from models.health_models import HealthOverviewResponse
router = APIRouter(prefix="/health", tags=["Health"])
  

router.get("/overview", response_model=HealthOverviewResponse, status_code=status.HTTP_200_OK) 
async def get_health_overview(
  current_user: User = Depends(get_current_active_user)
):
  """
  Retrieve a summary of the user's health data including sleep, activity, heart rate, and emotional wellbeing.
  """
  # Placeholder implementation
  return HealthOverviewResponse(
    sleep_hours=7.5,
    sleep_score=85,
    steps_count=10000,
    heart_rate=70,
    emotional_wellbeing_state="Good"
  )

