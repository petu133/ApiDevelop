from fastapi import Depends, status, HTTPException
from fastapi.security import OAuth2PasswordBearer
from jose import JWTError, jwt
from datetime import datetime, timedelta #timedelta() calculates differences in dates and allows the manipulation of it
from . import schemas

oauth2_bearer = OAuth2PasswordBearer(tokenUrl='login') #Paramater: the target url-endpoint 

MASTER_KEY = "09d25e094faa6ca2556c818166b7a9563b93f7099f6f0f4caa6cf63b88e8d3e7" #One of the most important features in the security flow
ALGO = "HS256"
TOKEN_EXPIRATION_MIN = 30

def create_access_token(data: dict): #the function takes in the payload that comes from the login path operation request.
    encode = data.copy() #Make a copy of the data. This ensure that the original information is not altered...
                     #"data" is a dictionary therefore the "encode" copy is a dict as well
    expire_time = datetime.utcnow() + timedelta(minutes=TOKEN_EXPIRATION_MIN) 
    #add the time expiration to the data that is going to be encoded within the jwt 
    encode.update({"exp": expire_time}) #important about the this method : "expire" WRONG | "exp" is the key that is needed in the logic to its correct execution
    jwt_value = jwt.encode(encode, MASTER_KEY, algorithm=ALGO) #the encode method takes in all the information we have above and generate the JSON Web Token
    return jwt_value

def verify_token(token: str, credential_exception): #Decode the received token, verify it, and return the current user.
                                                    #If the token is invalid, return an HTTP error right away.
    try:
        payload = jwt.decode(token, MASTER_KEY, algorithms=ALGO)
        id: str = payload.get("user_id") #Here the paramater is the data we embedded previously when called the create_access_token in the logic of the Login Path Operation
        if id is None:
            raise credential_exception
        token_data = schemas.TokenData(id = id)
    except JWTError:
        raise credential_exception
    return token_data    

#We can pass the next function as a dependency into anyone of the path operations, this way check the permissions of one user
def get_current_user(token: str = Depends(oauth2_bearer)):
    credential_exception = HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail=f"Wrong Credentials", headers={"WWW-Authenticate": "Bearer"})
    return verify_token(token, credential_exception)

    











