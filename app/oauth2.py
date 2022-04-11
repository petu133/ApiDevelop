from jose import JWTError, jwt
from datetime import datetime, timedelta #timedelta() calculates differences in dates and allows the manipulation of it

SECRET_KEY = "09d25e094faa6ca2556c818166b7a9563b93f7099f6f0f4caa6cf63b88e8d3e7" 
ALGO = "HS256"
TOKEN_EXPIRE_MINUTES = 30

def create_access_token(data: dict): #the function takes in the payload that comes from the login path operation request.
    encode = data.copy() #Make a copy of the data. This ensure that the original information is not altered...
                     #"data" is a dictionary therefore the "encode" copy is a dict as well
    expire_time = datetime.now() + timedelta(minutes=TOKEN_EXPIRE_MINUTES)
    
    #add the time expiration to the data that is going to be encoded within the jwt 
    encode.update({"exp": expire_time}) #important about the this method : "expire" WRONG | "exp" is the key that is needed in the logic to its correct execution
    
    jwt_value = jwt.encode(encode, SECRET_KEY, algorithm=ALGO) #the encode method takes in all the information we have above and generate the JSON Web Token

    return jwt_value







