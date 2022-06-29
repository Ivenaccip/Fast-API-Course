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

    email: EmailStr = Field(...,
                          example = 'ivenaccip@gmail.com')

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
                            example='Leonardo',)

    last_name: str = Field(...,
                           title='Last name',
                           min_length=2,
                           max_length=50,
                           example='Montaño',)

    birth_day: Optional[date] = Field(default=None,
                                       title='Birth date',
                                       example='2021-01-01',)

class UserRegister(User):
    password: str = Field(...,
                          min_length=8,
                          max_length=64,
                          example='password')

class Tweet(BaseModel):

    tweet_id: UUID = Field(...)

    content: str = Field(...,
                         min_length=1,
                         max_length=256,)

    created_at: datetime = Field(default=datetime.now())

    updated_at: Optional[datetime] = Field(default=None)

    by: User = Field(...)


# ============================================================
# Path operations
# ============================================================


@app.get('/',
         summary='Home',
         status_code=status.HTTP_200_OK)
def home():
    """
    Show users

    This path operation show all tweets in the app

    Parameters:
        - user : UserRegister

    Returns a json list with all tweets in the app, with the following keys:
        - user_id: UUID
        - email: Emailstr
        - first_name: str
        - last_name: str
        - birth_day: datetime
    """
    with open("users.json", "r", encoding="utf-8") as f:
        results = json.loads(f.read())
        return results

## Sing and login
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

### Show users
@app.get('/users/',
         response_model=List[User],
         status_code=status.HTTP_200_OK,
         summary='Show all users',
         tags=['Users'])
def show_users() -> List[User]:
    """
    Show users

    This path operation show all users in the app

    Parameters:
        - user : UserRegister

    Returns a json list with all users in the app, with the following keys:
        tweet_id: UUID
        content: str
        created_at: datetime
        updated_at: Optional[datetime]
        by: User
    """
    with open("tweets.json", "r", encoding="utf-8") as f:
        results = json.loads(f.read())
        return results

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


@app.post(
         path = '/tweets/',
         response_model=Tweet,
         status_code=status.HTTP_200_OK,
         summary='Post a tweet',
         tags=['Tweets'])
def list_tweets(tweet: Tweet = Body(...)):
    """
    Post a tweet

    This path operation post a tweet in the app

    Parameters:
        - Request Body Parameter:
            - tweet : Tweet

    Returns a json list with the basic tweet information:
        tweet_id: UUID
        content: str
        created_at: datetime
        updated_at: Optional[datetime]
        by: User
    """
    with open("tweets.json", "r+", encoding="utf_8") as f:
        results = json.loads(f.read())
        tweet_dict = tweet.dict()
        tweet_dict["tweet_id"] = str(tweet_dict["tweet_id"])
        tweet_dict["created_at"] = str(tweet_dict["created_at"])
        tweet_dict["updated_at"] = str(tweet_dict["updated_at"])
        tweet_dict["by"]["user_id"] = str(tweet_dict["by"]["user_id"])
        tweet_dict["by"]["birth_day"] = str(tweet_dict["by"]["birth_day"])
        results.append(tweet_dict)
        f.seek(0)
        f.write(json.dumps(results))
        return tweet


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