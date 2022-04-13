from fastapi import FastAPI
from fastapi import Response, status, HTTPException, Depends 
from typing import Optional, List
from fastapi.params import Body
from pydantic import BaseModel
from random import randrange
import psycopg2 #postgres database driver
from psycopg2.extras import RealDictCursor
import logging #logging package 
import time
from sqlalchemy.orm import Session
from .database import engine, get_db
from . import models, schemas, utils
from .routers import post, user, auth
#The fastapi library importation needs to be at the very top. This allows avoid some issues that could arise if not done in this way.

models.Base.metadata.create_all(bind=engine)

app = FastAPI()

while True:
    try:
        conn = psycopg2.connect(host='localhost', database='fastapi', user='postgres',
        password='systems133', cursor_factory=RealDictCursor)
        cursor = conn.cursor()
        print('The connection to database was successful')
        break
    except BaseException:
        logging.exception("An exception was thrown!")
        time.sleep(2)

# When an http request occurs, include these routers, then the request go to the folder routers where all the path operation logic inhabits
app.include_router(post.router) # the request search for a match in post, if it finds a match it's going to  respond as normally does
app.include_router(user.router) # same here -> 'grab the router object from the user file'
app.include_router(auth.router)
#This allows break out the code into separate files . I can't simply go and only imports the paths operations by themselves
# the router logic and its methods - include_router and APIRouter - are necessary for the correct execution of the FastApi app







