#from fastapi import FastAPI #move this import at the top of the application's files tends to avoid some errors to arise
from tkinter import CASCADE
from sqlalchemy.sql.expression import text
from sqlalchemy import Column, Integer, String, Boolean, ForeignKey
from sqlalchemy.orm import relationship
from .database import Base
from sqlalchemy.sql.sqltypes import TIMESTAMP

class Post(Base):
    __tablename__ = "posts" #This name will be the name of the table inside the database

    id = Column(Integer, primary_key = True, nullable = False) 
    title = Column(String, nullable = False) 
    content = Column(String, nullable = False) 
    published = Column(Boolean, server_default = 'TRUE', nullable = False)
    creation_time = Column(TIMESTAMP(timezone=True), server_default = text('now()'), nullable = False)
    id_owner = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable = False )
    owner_data = relationship("User") #tell sql akchemy to automatically fetch a piece of imformation based off of a relationship
                                      #Capital U letter(User) used because is referencing the class User, not the tablename 

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, nullable=False)
    mail = Column(String, nullable=False, unique=True)
    pw = Column(String, nullable=False)
    created = Column(TIMESTAMP(timezone=True), server_default = text('now()'), nullable = False)

class Vote(Base):
    __tablename__ = "votes"

    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), primary_key=True) #Together the user_id and post_id .. 
    post_id = Column(Integer, ForeignKey("posts.id", ondelete="CASCADE"), primary_key=True) #makes up a Composite Key


