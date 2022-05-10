from fastapi import Depends, status, HTTPException
from fastapi.security import OAuth2PasswordBearer
from jose import JWTError, jwt
from datetime import datetime, timedelta #timedelta() calculates differences in dates and allows the manipulation of it
from . import schemas, database, models
from sqlalchemy.orm import Session
from .config import settings

oauth2_bearer = OAuth2PasswordBearer(tokenUrl='login') #Paramater: the target url-endpoint 

MASTER_KEY = settings.master_key #One of the most important features in the security flow
ALGO = settings.algo
TOKEN_EXPIRATION_MIN = settings.token_expiration_min

def create_access_token(data: dict): #the function takes in the payload that comes from the login path operation request.
    encode = data.copy() #Make a copy of the data. This ensure that the original information is not altered...
                     #"data" is a dictionary therefore the "encode" copy is a dict as well
    expire_time = datetime.utcnow() + timedelta(minutes=TOKEN_EXPIRATION_MIN) 
#add the time expiration to the data that is going to be encoded within the jwt 
    encode.update({"exp": expire_time}) 
#important about the this method : "expire" WRONG | "exp" is the key that is needed in the logic to its correct execution
    
    jwt_value = jwt.encode(encode, MASTER_KEY, algorithm=ALGO) 
#the encode method takes in all the information we have above and generate the JSON Web Token
    return jwt_value

def verify_token(token: str, credential_exception): #Decode the received token, verify it, and return the current user.
                                                    #If the token is invalid, return an HTTP error right away.
    try:
        payload = jwt.decode(token, MASTER_KEY, algorithms=ALGO)
        id: str = payload.get("user_id") 
#Here the paramater "user id" is the data we embedded previously when called
#the create_access_token in the logic of the Login Path Operation
        
        if id is None:
            raise credential_exception
        token_data = schemas.TokenData(id = id)
    except JWTError:
        raise credential_exception
    return token_data    

#We can pass the next function as a dependency into anyone of the path operations, this way check the permissions of one user
def get_current_user(token: str = Depends(oauth2_bearer), db: Session = Depends(database.get_db)):
    credential_exception = HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
     detail=f"Wrong Credentials", headers={"WWW-Authenticate": "Bearer"})
   
    print(f"address memory of token bearer argument: {hex(id(token))}")
    print(f"token bearer value {token}")
    print(type(token))
    
    token = verify_token(token, credential_exception)
    
    print(f"address memory of token set variable: {hex(id(token))}")
    print(f"the value of the data is {token}")
    print(type(token))

    user = db.query(models.User).filter(models.User.id == token.id).first()
    
    print(user.created_at)
    print(user.password)
    print(user.id)
    print(user.mail)
   
    return user

    











