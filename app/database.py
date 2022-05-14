from fastapi import FastAPI 
#move FastApi import at the top of the application's files tends to avoid some errors to arise
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
# import psycopg2 #postgres database driver
# from psycopg2.extras import RealDictCursor
import time
import logging #logging package 
from .config import settings

#-- Set connection up to the database with sqlalchemy orm --
#SQLALCHEMY_DATABASE_URL = 'postgresql://<username>:<password>@<ip-address/hostname>/<database_name>'
SQLALCHEMY_DATABASE_URL = f'postgresql://{settings.database_username}:{settings.database_password}@{settings.database_hostname}:{settings.database_port}/{settings.database_name}'


print(f"The database name is {settings.database_name}")
print(type({settings.database_name}))

engine = create_engine(SQLALCHEMY_DATABASE_URL,  pool_pre_ping=True, 
              pool_recycle=3600, # this line might not be needed
              connect_args={
                  "keepalives": 1,
                  "keepalives_idle": 30,
                  "keepalives_interval": 10,
                  "keepalives_count": 5,
              })

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
#-- set up finished --

# while True:
#     try:
#         conn = psycopg2.connect(host='localhost', database='fastapi', user='postgres',
#         password='systems133', cursor_factory=RealDictCursor)
#         cursor = conn.cursor()              
#         print('The connection to database was successful')
#         break
#     except BaseException:
#         logging.exception("An exception was thrown!")
#         time.sleep(2)
#-- connecting to the database with regular psycopg sql driver (could be commented without break the app 
#since we have sql mananing the connection within database.py file) allows run raw sql                