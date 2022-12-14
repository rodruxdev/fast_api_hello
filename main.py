# Python
from typing import Optional
from enum import Enum
# Pydantic
from pydantic import BaseModel
from pydantic import Field
from pydantic import EmailStr
#Fast API
from fastapi import FastAPI
from fastapi import status
from fastapi import HTTPException
from fastapi import Body, Query, Path, Form, Header, Cookie, File, UploadFile

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

class UserBase(BaseModel):
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


class User(UserBase):
  password: str = Field(..., min_length=8)

  class Config:
    schema_extra = {
      "example": {
        "first_name": "Rodrigo",
        "last_name": "Goitia",
        "age": 24,
        "hair_color": "black",
        "is_married": False,
        "password": "EsteEsUnPassword"
      }
    }


class UserOut(UserBase):
  pass


class LoginOut(BaseModel):
  username: str = Field(..., max_length=20, example="rodruxdev")
  message: str = Field(default='Login successful')

@app.get(
  path="/",
  status_code=status.HTTP_200_OK,
  tags=["Home"]
  )
def home():
  return {"Hello": "World"}

# Request and Response Body
@app.post(
  path="/user/new",
  response_model=UserOut,
  status_code=status.HTTP_201_CREATED,
  tags=["Users"],
  summary="Create user in the app"
  )
def create_user(user: User = Body(...)):
  """
  Create User

  This path operation creates a user in the app and save the information in the database

  Parameters:
  - Request body parameter
    - **person: Person** -> A person model with first name, last name, age, hair color and marital status.

  Returns a person model with first name, last name, age, hair color and marital status.
  """
  return user

# Validations Query Parameters

@app.get(
  path="/user/detail/",
  status_code=status.HTTP_200_OK,
  tags=["Users"],
  deprecated=True
)
def show_user(
  name: Optional[str] = Query(
    None,
    min_length=1,
    max_length=50,
    title="User Name",
    description="This is the user's name. It's between 1 and 50 characters",
    example="Roc??o"
    ),
  age: int = Query(
    ...,
    title="User Age",
    description="This is the person age. It's required",
    example=25
    )
):
  return {name: age}

users = [1, 2, 3, 4, 5]

@app.get(
  path="/user/detail/{user_id}",
  status_code=status.HTTP_200_OK,
  tags=["Users"]
  )
def show_user(
  user_id: int = Path(
    ...,
    gt=0,
    title="User ID",
    description="This is the user ID, It's a required integer and grater than 0",
    example=123
    )
):
  if user_id not in users:
    raise HTTPException(
      status_code=status.HTTP_404_NOT_FOUND,
      detail="This user doesn't exists."
    )
  return {user_id: "It exists!"}

@app.put(
  path="/user/{user_id}",
  status_code=status.HTTP_202_ACCEPTED,
  tags=["Users"]
  )
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

# Forms

@app.post(
  path="/login",
  response_model=LoginOut,
  status_code=status.HTTP_200_OK,
  tags=["Users"]
)
def login(username: str = Form(...), password: str = Form(...)):
  return LoginOut(username=username)

# Cookies and Headers Parameters
@app.post(
  path="/contact",
  status_code=status.HTTP_200_OK,
  tags=["Contact"]
)
def contact(
  first_name: str = Form(
    ...,
    max_length=20,
    min_length=1,
  ),
  last_name: str = Form(
    ...,
    max_length=20,
    min_length=1,
  ),
  email: EmailStr = Form(...),
  message: str = Form(
    ...,
    min_length=20
  ),
  user_agent: Optional[str] = Header(default=None),
  ads: Optional[str] = Cookie(default=None),
):
  return {"user_agent": user_agent, "ads": ads}

# Files

@app.post(
  path="/post-image",
  tags=["Images"]
)
def post_image(
  image: UploadFile = File(...)
):
  return {
    "Filename": image.filename,
    "Format": image.content_type,
    "Size(kb)": round(len(image.file.read())/1024, ndigits=2)
  }