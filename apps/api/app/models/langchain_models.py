from pydantic import BaseModel

class ContextData(BaseModel):
  user_id: str