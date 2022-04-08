from fastapi import FastAPI
from passlib.context import CryptContext

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto") # it informs to passlib about the hashing method

def hash(password: str):
    pwd_context.hash(password)






