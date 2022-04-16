#from fastapi import FastAPI #move this import at the top of the application's files tends to avoid some errors to arise
from sqlalchemy.sql.expression import text
from sqlalchemy import Column, Integer, String, Boolean, ForeignKey
from sqlalchemy.orm import relationship
from .database import Base
from sqlalchemy.sql.sqltypes import TIMESTAMP

class Post(Base):
    __tablename__ = "posts"

    id = Column(Integer, primary_key = True, nullable = False) 
    title = Column(String, nullable = False) 
    content = Column(String, nullable = False) 
    published = Column(Boolean, server_default = 'TRUE', nullable = False)
    created_at = Column(TIMESTAMP(timezone=True), server_default = text('now()'), nullable = False)
    owner_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable = False )
    owner_data = relationship("User")        #tell sql akchemy to automatically fetch a piece of imformation based off of a relationship
            #Capital (User) because is referencing the class User, not the tablename

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, nullable=False)
    email = Column(String, nullable=False, unique=True)
    password = Column(String, nullable=False)
    created_at = Column(TIMESTAMP(timezone=True), server_default = text('now()'), nullable = False)




