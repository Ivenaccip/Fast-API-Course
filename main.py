# Python
from encodings import utf_8
from uuid import UUID
from datetime import date
from datetime import datetime
from typing import Dict
from typing import List
from typing import Optional

# Pydantic
from pydantic import BaseModel
from pydantic import EmailStr
from pydantic import Field

# FastAPI
from fastapi import FastAPI
from fastapi import status
from fastapi import Path
from fastapi import Body

#json
import json

# Initialize the app
app = FastAPI()


# ============================================================
# Define models
# ============================================================

class UserBase(BaseModel):

    user_id: UUID = Field(...,)

    email: EmailStr = Field(...,)

class UserLogin(UserBase):

    password: str = Field(...,
                          min_length=8,
                          max_length=64,
                          example='password')

class User(UserBase):

    first_name: str = Field(...,
                            title='First name',
                            min_length=2,
                            max_length=50,
                            example='John',)

    last_name: str = Field(...,
                           title='Last name',
                           min_length=2,
                           max_length=50,
                           example='Doe',)

    birth_day: Optional[date] = Field(default=None,
                                       title='Birth date',
                                       example='2021-01-01',)

class UserRegister(User):
    password: str = Field(...,
                          min_length=8,
                          max_length=64,
                          example='password')


class Tweet(BaseModel):

    id: UUID = Field(...)

    content: str = Field(...,
                         min_length=1,
                         max_length=256,)

    created_at: datetime = Field(default=datetime.now(),
                                title='Creation date',
                                example='2020-01-01T00:00:00Z',)

    updated_at: Optional[datetime] = Field(default=None,
                                           title='Last update date',
                                           example='2020-01-01T00:00:00Z',)

    created_by: User = Field(...,
                             title='User who created the tweet',)


# ============================================================
# Path operations
# ============================================================


@app.get('/',
         summary='Home',
         status_code=status.HTTP_200_OK)
def home() -> Dict[str, str]:
    """Home route.

    Returns a message indicating that the app is running.
    """

    return {
        'message': 'Twitter API is working!',
    }


## Auth
@app.post('/signup',
          response_model=User,
          status_code=status.HTTP_201_CREATED,
          summary='Sign up',
          tags=['Users'])
def signup(user: UserRegister = Body(...)):
    """
    Signup

    This path operation register an user in the app

    Parameters:
        - Request body parameter
            - user : UserRegister

    Returns a json with the basic user information:
        - user_id: UUID
        - email: Emailstr
        - first_name: str
        - last_name: str
        - birth_day: datetime
    """
    with open("users.json", "r+", encoding="utf_8") as f:
        results = json.loads(f.read())
        user_dict = user.dict()
        user_dict["user_id"] = str(user_dict["user_id"])
        user_dict["birth_day"] = str(user_dict["birth_day"])
        results.append(user_dict)
        f.seek(0)
        f.write(json.dumps(results))
        return user


@app.post('/login',
          response_model=UserLogin,
          status_code=status.HTTP_200_OK,
          summary='Login',
          tags=['Users'])
def login(user: User):
    pass


## Users

@app.get('/users/',
         response_model=List[User],
         status_code=status.HTTP_200_OK,
         summary='Get all users',
         tags=['Users'])
def list_users() -> List[User]:
    pass


@app.get('/users/{id}',
         response_model=User,
         status_code=status.HTTP_200_OK,
         summary='Get a user',
         tags=['Users'])
def retrieve_user(
    id: int = Path(...,
                   gt=0,
                   title='User ID',
                   description='The ID of the user to retrieve',
                   example=1,),
) -> User:
    pass


@app.put('/users/{id}',
         response_model=User,
         status_code=status.HTTP_200_OK,
         summary='Update user',
         tags=['Users'])
def update_user(
    id: int = Path(...,
                   gt=0,
                   title='User ID',
                   description='The ID of the user to update',
                   example=1,),
) -> User:
    pass


@app.delete('/users/{id}',
            status_code=status.HTTP_204_NO_CONTENT,
            summary='Delete user',
            tags=['Users'])
def delete_user(
    id: int = Path(...,
                   gt=0,
                   title='User ID',
                   description='The ID of the user to update',
                   example=1,),
) -> User:
    pass


## Tweets


@app.get('/tweets/',
         response_model=List[Tweet],
         status_code=status.HTTP_200_OK,
         summary='Get all tweets',
         tags=['Tweets'])
def list_tweets() -> List[Tweet]:
    pass


@app.get('/tweets/{id}',
         response_model=Tweet,
         status_code=status.HTTP_200_OK,
         summary='Get a tweet',
         tags=['Tweets'])
def retrieve_tweet(
    id: int = Path(...,
                   gt=0,
                   title='Tweet ID',
                   description='The ID of the tweet to retrieve',
                   example=1,),
) -> Tweet:
    pass


@app.put('/tweets/{id}',
         response_model=Tweet,
         status_code=status.HTTP_200_OK,
         summary='Update tweet',
         tags=['Tweets'])
def update_tweet(
    id: int = Path(...,
                   gt=0,
                   title='Tweet ID',
                   description='The ID of the tweet to update',
                   example=1,),
) -> Tweet:
    pass


@app.delete('/tweets/{id}',
            status_code=status.HTTP_204_NO_CONTENT,
            summary='Delete tweet',
            tags=['Tweets'])
def delete_tweet(
    id: int = Path(...,
                   gt=0,
                   title='Tweet ID',
                   description='The ID of the tweet to update',
                   example=1,),
) -> Tweet:
    pass