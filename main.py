# Python
from typing import Optional
# Pydantic
from pydantic import BaseModel
#Fast API
from fastapi import FastAPI
from fastapi import Body
from fastapi import Query

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
  name: Optional[str] = Query(None, min_length=1, max_length=50),
  age: str = Query(...)
):
  return {name: age}