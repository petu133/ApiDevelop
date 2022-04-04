from fastapi import FastAPI, Response, status, HTTPException, Depends
from typing import Optional
from fastapi.params import Body
from pydantic import BaseModel
from random import randrange
import psycopg2 #postgres database driver
from psycopg2.extras import RealDictCursor
import logging #logging package 
import time
from sqlalchemy.orm import Session
from . import models
from .database import engine, get_db


models.Base.metadata.create_all(bind=engine)

app = FastAPI()

class Post(BaseModel):
    title: str
    content: str
    published: bool = True #set True * by default (only in case the user don't type any information about the field)    
    rating: Optional[int] = None #set None *

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

my_posts = [{"title": "this is the title", "content": "this is the content", "id": 1}, {"title": "this is the title2", "content": "this is the content2", "id": 2}]    #there isn't database yet, so this is hardcode data in the program's memory

def find_post(id):
    for p in my_posts:
        if p['id'] == id:
            return p

def find_index_post(id):
    for i, p in enumerate(my_posts):
        if p['id'] == id:
            #print(i) The count of the indexes in the iterable created with enumerate method
            #print(p) The element of the values's group
            return i #return the count of the iterable (in this case de list of dictionaries) that match the id provide by the user

@app.get("/")
def root():
    return {"message": "Hello Index World"}

@app.get("/sqlalchemy")
def test_posts(db: Session = Depends(get_db)):
    
    return {"message":"success"}

@app.get("/posts")
def get_posts():
    cursor.execute(""" SELECT * FROM posts """)
    posts = cursor.fetchall()
    return {"data": posts}
    #return {"data": my_posts} #working with array in local memory

""" Without Base Model (pedantic library)
@app.post("/post")
def create_post(payload: dict = Body(...)) -> dict: 
    # Usage of hints for pseudo-static check of data types (similar to an regular static language) inside the argument and the expected output of the function
    print(payload)
    return {"new_post" : f"title : {payload['title']} content : {payload['content']}"}
"""

@app.post("/posts", status_code=status.HTTP_201_CREATED)  #inside the decorator - change the default status code of the specific path operation
def create_posts(new_post: Post):
    # Not use string interpolation (f"{}"") is vulnerable to sql injection.
    cursor.execute("""INSERT INTO posts (title, content, published) VALUES (%s,%s,%s) RETURNING * """, (new_post.title, new_post.content, new_post.published)) #use placeholders variables provided by psycopg2 library module 
    my_new_post = cursor.fetchone()
    conn.commit() # raise the data to the postgress database
    return {"data" : my_new_post}
    #post_dict = new_post.dict()         # (first intent) working with array in local memory
    #post_dict['id'] = randrange(1,1000)
    #my_posts.append(post_dict)
    #return {"data" : post_dict}

"""
@app.get("/posts/{id}")  
def get_post(id):   #No invalid id value issue handled . Below ("/posts/{id}")  calls do have error handling
    post = find_post(int(id))
    return {"post_details": post}
"""
"""
@app.get("/posts/{id}")
def get_post(id: int, response: Response): #id is declared to be an int - response is declared to be a Response's class element
    post = find_post(id)
    if not post:
        response.status_code = status.HTTP_404_NOT_FOUND
        return {"message": f"post with id: {id} was no found"}
    return {"post_details": post}
"""
@app.get("/posts/{id}") #The data parameter 'id' comes in like a String
def get_post(id: int): #id converted to be an int. Avoid misspell in the path paramater by the user
    cursor.execute("""SELECT * FROM posts WHERE id = %s""", (str(id),)) #SQL statament only accepts string || the comma after solves some possible issues that could occur
    post = cursor.fetchone()
    #post = find_post(id) (first intent) working with array in local memory
    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail= f"post with id: {id} was no found")
    return {"post_details": post}

@app.delete("/posts/{id}", status_code=status.HTTP_204_NO_CONTENT) 
def delete_post(id: int):
    #index = find_index_post(id) (first intent) working with array in local memory
    cursor.execute("""DELETE FROM posts WHERE id = %s returning *""", (str(id),))
    deleted_post = cursor.fetchone()
    conn.commit()
    print(type(delete_post))
    #if index == None:
    if deleted_post == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)
    #my_posts.pop(index)
    return Response(status_code=status.HTTP_204_NO_CONTENT) #Restful HTTP Status 204 (No Content) MUST NOT include a message body

@app.put("/posts/{id}")
def update_post(id: int, post: Post):
    #index = find_index_post(id)
    cursor.execute("""UPDATE posts SET title = %s, content = %s, published = %s WHERE id = %s RETURNING *""", (post.title, post.content, post.published, str(id)))
    updated_post = cursor.fetchone()
    print(updated_post)
    print(type(updated_post))
    conn.commit()
    #if index == None: #if not index - - works but there was an issue handlilng the zero index of the list my_posts[] 
    if updated_post == None: 
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)
    return {"message" : updated_post}
    #post_dict = post.dict()
    #post_dict['id'] = id
    #my_posts[index] = post_dict
    #return {"message" : post_dict}
    