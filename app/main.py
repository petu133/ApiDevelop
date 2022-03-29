from turtle import pos
from fastapi import FastAPI, Response, status, HTTPException
from fastapi.params import Body
from pydantic import BaseModel
from typing import Optional
from random import randrange

app = FastAPI()

class Post(BaseModel):
    title: str
    content: str
    published: bool = True #set True * by default (only in case the user don't type any information about the field)    
    rating: Optional[int] = None #set None *

#there isn't database yet, so this is hardcode data in the program's memory
my_posts = [{"title": "this is the title", "content": "this is the content", "id": 1}, {"title": "this is the title2", "content": "this is the content2", "id": 2}]    

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

@app.get("/posts")
def get_posts():
    return {"data": my_posts}

""" Without Base Model (pedantic library)
@app.post("/post")
def create_post(payload: dict = Body(...)) -> dict: 
    # Usage of hints for pseudo-static check of data types (similar to an regular static language) inside the argument and the expected output of the function
    print(payload)
    return {"new_post" : f"title : {payload['title']} content : {payload['content']}"}
"""

@app.post("/posts", status_code=status.HTTP_201_CREATED)  #inside the decorator - change the default status code of the specific path operation
def create_posts(new_post: Post):
   # print(new_post)
   # print("The data-type of the above is: ", type(new_post))
    post_dict = new_post.dict()
    #print(post_dict)
   # print("The data-type of the above is: ", type(post_dict))
    post_dict['id'] = randrange(1,1000)
    my_posts.append(post_dict)
    return {"data" : post_dict}

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
@app.get("/posts/{id}")
def get_post(id: int): #In this case, id is declared to be an int. 
    post = find_post(id)
    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail= f"post with id: {id} was no found")
    return {"post_details": post}

@app.delete("/posts/{id}", status_code=status.HTTP_204_NO_CONTENT) 
def delete_post(id: int):
    index = find_index_post(id)
    if index == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)
    my_posts.pop(index)
    return Response(status_code=status.HTTP_204_NO_CONTENT) #Restful HTTP Status 204 (No Content) MUST NOT include a message body

@app.put("/posts/{id}")
def update_post(id: int, post: Post):
    index = find_index_post(id)
    if index == None: #if not index - - works but there was an issue handlilng the zero index of the list my_posts[] 
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)
    post_dict = post.dict()
    post_dict['id'] = id
    my_posts[index] = post_dict
    return {"message" : post_dict}