from fastapi import APIRouter, Depends, status, HTTPException, Response
from .. import schemas, models, utils, database, oauth2
from sqlalchemy.orm import Session
#from ..database import get_db

router = APIRouter(tags=['Authentication'])

@router.post('/login')
def login(user_credentials: schemas.UserLogin, db: Session = Depends(database.get_db)):
    
    #catch the data from the database that matches with the credential passed by the user
    user = db.query(models.User).filter(models.User.email == user_credentials.email).first() 
    
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Invalid Credentials")

    if not utils.verify(user_credentials.password, user.password):
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Invalid Credentials")
    
    token = oauth2.create_access_token(data={"user_id" : user.id}) #grab the id of the user from the database (already obtained via query above)
    #the passed can be more than only that (maybe data about the permissions to access several paths)
    return {"token" : token, "token_type" : "bearer"}  

    
    













