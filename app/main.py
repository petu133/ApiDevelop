from fastapi import FastAPI 
#The fastapi library importation needs to be at the very top. This allows avoid some issues that could arise if not done in this way.
from fastapi.middleware.cors import CORSMiddleware
from random import randrange
from .database import engine
from . import models
from .routers import post, user, auth, vote
from .config import Settings

#--cmd commands-- venv\Scripts\activate.bat  "Enter to the environment"
# uvicorn app.main:app --reload  "Reads app setting variable in main.py and executes the fastapi program"

#models.Base.metadata.create_all(bind=engine) 
#Tells sql alchemy to run the create statement so that it generates the tables.
#Since I executed all that logic from alembic, the line can be commnented. 


app = FastAPI()

#origins = ["https://www.google.com"] #Allows google to talk to our API, so not only the server domain can do it
origins = ["*"] #Allows all sites to talk to our API
app.add_middleware(
    CORSMiddleware, #(In WebFrameworks) can think of a Middleware as some sort of function that runs before every request
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# When an http request occurs, include these routers, then the request go 
# to the folder routers where all the path operation logic inhabits

app.include_router(post.router) 
# the request search for a match in post, if it finds a match it's going to  respond as normally does
app.include_router(user.router) 
# same here -> 'grab the router object from the user file'

app.include_router(auth.router)
app.include_router(vote.router)
#This allows break out the code into separate files . I can't simply go and only imports the paths 
#operations by themselves the router logic and its methods - include_router and APIRouter - 
# are necessary for the correct execution of the FastApi app







