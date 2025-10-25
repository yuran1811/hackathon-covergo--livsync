from typing import Union

from fastapi import FastAPI

from app.dependencies.langchain import create_ai_insights

app = FastAPI()


@app.get("/")
def read_root():
    return {"Hello": "World"}

@app.get("/items/{item_id}")
def read_item(item_id: int, q: Union[str, None] = None):
    return {"item_id": item_id, "q": q}

@app.get("/users/{user_id}")
def read_user(user_id: str):
    return create_ai_insights(user_id=user_id)
