from datetime import datetime
from pydantic import BaseModel, EmailStr

class PostBase(BaseModel):
    title: str
    content: str
    published: bool = True #set True * by default (only in case the user don't type any information about the field)

class PostCreate(PostBase):
    pass

class Post(PostBase): #schema for the Response Server -> User/Frontend
    id: int            #Here i can specify exactly what field i want to send in the response's body 
    created_at: datetime
    # title , content and published fields inherit from PostBase
    class Config:
        orm_mode = True #Pydantic's orm_mode will tell the Pydantic model to read the data even if it is not a dict but an ORM model...
                        #(or any other arbitrary object with attributes). Fast Api documentation web site SOURCE:https://fastapi.tiangolo.com/tutorial/sql-databases/

class UserCreate(BaseModel):
    email: EmailStr
    password: str 

class UserOut(BaseModel): #I don't want to send back to the user his password.
    id: int
    email: EmailStr
    created_at: datetime
    class Config:                  #And with this, the Pydantic model is compatible with ORMs ... 
        orm_mode = True  #and you can just declare it in the response_model argument in your path operations.

class UserLogin(BaseModel):
    email: EmailStr
    password: str


