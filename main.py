# Python
from typing import Optional
# Pydantic
from pydantic import BaseModel
#Fast API
from fastapi import FastAPI
from fastapi import Body, Query, Path

app = FastAPI()

#Models

class User(BaseModel):
  first_name: str
  last_name: str
  age: int
  hair_color: Optional[str] = None
  is_married: Optional[bool] = None

@app.get("/")
def home():
  return {"Hello": "World"}

# Request and Response Body
@app.post("/user/new")
def create_user(user: User = Body(...)):
  return user

  # Validations Query Parameters

@app.get("/user/detail/")
def show_user(
  name: Optional[str] = Query(
    None,
    min_length=1,
    max_length=50,
    title="User Name",
    description="This is the user's name. It's between 1 and 50 characters"
    ),
  age: str = Query(
    ...,
    title="User Age",
    description="This is the person age. It's required"
    )
):
  return {name: age}

@app.get("/user/detail/{user_id}")
def show_user(
  user_id: int = Path(
    ...,
    gt=0,
    title="User ID",
    description="This is the user ID, It's a required integer and grater than 0"
    )
):
  return {user_id: "It exists!"}