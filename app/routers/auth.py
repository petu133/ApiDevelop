from fastapi import APIRouter, Depends, status, HTTPException, Response
from fastapi.security.oauth2 import OAuth2PasswordRequestForm
from .. import schemas, models, utils, database, oauth2
from sqlalchemy.orm import Session


router = APIRouter(tags=['Authentication'])

@router.post('/login')
def login(user_credentials: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(database.get_db)):
    
    #OAuth2PasswordRequestFrom stores de data as a dictionary. 
    # {
    #     "username" : " ",  Whatever value the user pass (email, pen name, id, etc)
    #     "password" : " "
    # }
    # Now in Postman the credentials are no longer pass in through raw json on the body. Instead we pass it as form-data.

    #Catch the data from the database that matches with the credential passed by the user
    user = db.query(models.User).filter(models.User.email == user_credentials.username).first() 
    
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Invalid Credentials")

    if not utils.verify(user_credentials.password, user.password):
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Invalid Credentials")
    
    token = oauth2.create_access_token(data={"user_id" : user.id}) #grab the id of the user from the database (already obtained via query above)
    #the passed can be more than only that (maybe data about the permissions to access several paths)
    return {"token" : token, "token_type" : "bearer"}  

    
    













