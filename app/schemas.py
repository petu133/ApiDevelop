from datetime import datetime
from pydantic import BaseModel, EmailStr
from typing import Optional
from pydantic.types import conint
from sqlalchemy import Integer

# A schema is used to validate data we receive as well as to reformat the data that we want to send to the client/browser.
# Because there is no way we can trust the users/frontend. The users may send anything they want and we don't want to store it without verifying.

class PostBase(BaseModel):
    title: str
    content: str
    published: bool = True #set True * by default (only in case the user don't type any information about the field)

class PostCreate(PostBase):
    pass

class UserOut(BaseModel): #I don't want to send back to the user his password.
    id: int
    email: EmailStr
    created_at: datetime
    class Config:        #And with this, the Pydantic model is compatible with ORMs ... 
        orm_mode = True  #and you can just declare it in the response_model argument in your path operations.

class Post(PostBase): #schema for the Response Server -> User/Frontend
    id: int           #Here i can specify exactly what field i want to send in the response's body 
    created_at: datetime
    owner_id: int
    owner_data: UserOut    #return a pydantic model type . UserOut class need to be above so python properly reads it
    # title , content and published fields inherit from PostBase
    class Config:
        orm_mode = True #Pydantic's orm_mode will tell the Pydantic model to read the data even if it is not a dict but an ORM model...
                        #(or any other arbitrary object with attributes). Fast Api documentation web site SOURCE:https://fastapi.tiangolo.com/tutorial/sql-databases/

class UserCreate(BaseModel):
    email: EmailStr
    password: str 

class UserLogin(BaseModel):
    email: EmailStr
    password: str

class Token(BaseModel):
    token: str
    token_type: str

class TokenData(BaseModel):
    id: Optional[str] = None   

class Vote(BaseModel):
    post_id: int
    dir: conint(le=1) #less than or equal to one







