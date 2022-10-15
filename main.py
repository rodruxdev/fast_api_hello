# Python
from typing import Optional
from enum import Enum
# Pydantic
from pydantic import BaseModel
from pydantic import Field
#Fast API
from fastapi import FastAPI
from fastapi import Body, Query, Path

app = FastAPI()

#Models

class HairColor(Enum):
  white = "white"
  brown = "brown"
  black = "black"
  blonde = "blonde"
  red = "red"


class Location(BaseModel):
  city: str
  state: str
  country: str


class User(BaseModel):
  first_name: str = Field(
    ...,
    min_length=1,
    max_length=50
  )
  last_name: str = Field(
    ...,
    min_length=1,
    max_length=50
  )
  age: int = Field(
    ...,
    gt=0,
    le=115,
  )
  hair_color: Optional[HairColor] = Field(default=None)
  is_married: Optional[bool] = Field(default=None)

  class Config:
    schema_extra = {
      "example": {
        "first_name": "Rodrigo",
        "last_name": "Goitia",
        "age": 24,
        "hair_color": "black",
        "is_married": False
      }
    }


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
    description="This is the user's name. It's between 1 and 50 characters",
    example="Rocío"
    ),
  age: int = Query(
    ...,
    title="User Age",
    description="This is the person age. It's required",
    example=25
    )
):
  return {name: age}

@app.get("/user/detail/{user_id}")
def show_user(
  user_id: int = Path(
    ...,
    gt=0,
    title="User ID",
    description="This is the user ID, It's a required integer and grater than 0",
    example=123
    )
):
  return {user_id: "It exists!"}

@app.put("/user/{user_id}")
def update_user(
  user_id: int = Path(
    ...,
    gt=0,
    title="User ID",
    description="This is the user ID, It's a required integer and grater than 0",
    example=123
  ),
  user: User = Body(...),
  location: Location = Body(...)
):
  return {
    "user": user,
    "location": location
  }