from fastapi import FastAPI #The fastapi library importation needs to be at the very top. This allows avoid some issues that could arise if not done in this way.
from random import randrange
from .database import engine
from . import models
from .routers import post, user, auth
from .config import Settings
 
models.Base.metadata.create_all(bind=engine)

app = FastAPI()

# When an http request occurs, include these routers, then the request go to the folder routers where all the path operation logic inhabits
app.include_router(post.router) # the request search for a match in post, if it finds a match it's going to  respond as normally does
app.include_router(user.router) # same here -> 'grab the router object from the user file'
app.include_router(auth.router)
#This allows break out the code into separate files . I can't simply go and only imports the paths operations by themselves
# the router logic and its methods - include_router and APIRouter - are necessary for the correct execution of the FastApi app







