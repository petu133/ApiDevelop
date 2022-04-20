from fastapi import Response, status, HTTPException, Depends, APIRouter
from sqlalchemy.orm import Session
from typing import List, Optional  # This library allows the type checker handles type hints
from .. import models, schemas, oauth2, utils
from ..database import get_db

router = APIRouter(   #router object allows to split up different path operation into distinc files      
    prefix="/posts",
    tags=['Posts'] #groups the paths by category inside the auto-generated Swagger UI documentation
    ) 

my_posts = [{"title": "this is the title", "content": "this is the content", "id": 1}, {"title": "this is the title2", "content": "this is the content2", "id": 2}]    #there isn't database yet, so this is hardcode data in the program's memory

def find_post(id): #Auxiliar method for working with the array store in local memory
    for p in my_posts:
        if p['id'] == id:
            return p

def find_index_post(id): #Auxiliar method for working with the array store in local memory
    for i, p in enumerate(my_posts):
        if p['id'] == id:
            #print(i) The count of the indexes in the iterable created with enumerate method
            #print(p) The element of the values's group
            return i #return the count of the iterable (in this case de list of dictionaries) that match the id provide by the user

# @router.get("/")
# def root():
#      return {"message": "Hello Index World"}

@router.get("/sqlalchemy")
def test_posts(db: Session = Depends(get_db)):
    #db.query(models.Post) --- Makes an query as sql plain text. Then turns out that if you print this, shows up in console  "SELECT posts.id AS posts_id, posts.title AS posts_title, posts.content AS posts_content, posts.published AS posts_published, posts.created_at AS posts_created_at FROM posts""
    posts = db.query(models.Post).all()
    #print(type(posts), f"posts var contains the following entries from the database : {posts}")
    #print(f"The address in memory for the post variable is {id(posts)}")
    return {"data": "hardcoded info"} #hardcoded response to the client

@router.get("/", response_model=List[schemas.Post]) # Here my response is a list of our specific schema post model, that's why i need the import of List from typing
def get_posts(db: Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user), limit: int = 10, skip: int = 0, search: Optional[str] = ""): #current_user type doesn't matter int this case, can be int, dict, whatever, does not impact not at all || set "limit" as being a query parameter, default value = 10
    # cursor.execute(""" SELECT * FROM posts """) #working with raw sql and the psycopg2 database driver
    # posts = cursor.fetchall()
    print(f"query paramater limit value is: {limit}")
# -- working with sqlalchemy ORM--= 
    posts = db.query(models.Post).filter(models.Post.title.contains(search)).limit(limit).offset(skip).all() # offset allow to skip over a specific number of posts. This is util for implement Pagination on the frontend
    #return {"data": posts}
    return posts # retuning multiple posts, not only one

    #return {"data": my_posts} #working with array in local memory

""" Without Base Model (pedantic library)
@app.post("/post")
def create_post(payload: dict = Body(...)) -> dict: 
    # Usage of hints for pseudo-static check of data types (similar to an regular static language) inside the argument and the expected output of the function
    print(payload)
    return {"new_post" : f"title : {payload['title']} content : {payload['content']}"} The dict returned by the function
"""

@router.post("/", status_code=status.HTTP_201_CREATED, response_model=schemas.Post)  #inside the decorator - change the default status code of the specific path operation
def create_posts(new_post: schemas.PostCreate, db: Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user)): #get current user is gonna be a dependency that forces the user to have to be logged to create a post.
# ---working with raw sql and the psycopg2 database driver---
    # cursor.execute("""INSERT INTO posts (title, content, published) VALUES (%s,%s,%s) RETURNING * """, (new_post.title, new_post.content, new_post.published)) #use placeholders variables provided by psycopg2 library module . NOT use string interpolation (f"{}"") because it is vulnerable to sql injection
    # my_new_post = cursor.fetchone()
    # conn.commit() # raise the data to the postgress database, commit the changes that're above
    # return {"data" : my_new_post}

#--working with sqlalchemy ORM--
    print(f"In this operation -create post- the user id was: {current_user.id}") #This data comes from the authentication process
    print(f"Also the user email is: {current_user.email}")
    #my_new_post = models.Post(title=new_post.title, content=new_post.content, published=new_post.published) 
    my_new_post = models.Post(owner_id=current_user.id, **new_post.dict()) #we want to create a new post by referencing the Post's model. Convert new_post to a dictionary and unpack it with the ** operator (UNPACKING OPERATOR for dictionary). Useful to manipulate lot of columns nor a few. Make the inside of the method argument much less verbose
  # So what * (single star) does is to expand all items available in an iterable, for example list or tuple. And what ** (double star) does is to expand all available keyword arguments in a dictionary for example. source : https://www.quora.com/What-is-the-difference-between-the-and-operators-in-Python-1
    print(f"data passed was ...  {new_post}")
    db.add(my_new_post)
    db.commit() # raise the data to the postgress database, commit the changes that're above
    db.refresh(my_new_post) #Since we didn't supply a RETURNING sql statament we need to refresh to retrieve de new inserted data 
    
    return my_new_post
   
    #post_dict = new_post.dict()         # (first intent) working with array in local memory
    #post_dict['id'] = randrange(1,1000)
    #my_posts.append(post_dict)
    #return {"data" : post_dict}

"""
@app.get("/{id}")  
def get_post(id):   #No invalid id value issue handled . Below ("/posts/{id}")  calls do have error handling
    post = find_post(int(id))
    return {"post_details": post}
"""
"""
@app.get("/{id}")  #working with array in local memory
def get_post(id: int, response: Response): #id is declared to be an int - response is declared to be a Response's class element
    post = find_post(id)
    if not post:
        response.status_code = status.HTTP_404_NOT_FOUND
        return {"message": f"post with id: {id} was no found"}
    return {"post_details": post}
"""
@router.get("/{id}", response_model=schemas.Post) #The data parameter 'id' comes in like a String. Here Id is acting as a path parameter.
def get_post(id: int, db: Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user)): #id converted to be an int. Avoid misspell in the path paramater by the user
#---working with raw sql and the psycopg2 database driver---    
    # cursor.execute("""SELECT * FROM posts WHERE id = %s""", (str(id),)) #SQL statament only accepts string || the comma after solves some possible issues that could occur
    # post = cursor.fetchone()
#     if not post:
#         raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail= f"post with id: {id} was no found")

#--working with sqlalchemy--
    post = db.query(models.Post).filter(models.Post.id == id).first()   
    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail= f"post with id: {id} was no found")
    return post


@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT) 
def delete_post(id: int,db: Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user)):
#---working with raw sql and the psycopg2 database driver---       
    # cursor.execute("""DELETE FROM posts WHERE id = %s returning *""", (str(id),))
    # deleted_post = cursor.fetchone()
    # conn.commit()
    # if deleted_post == None:
    #     raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)

#working with sqlalchemy ORM
    post_query = db.query(models.Post).filter(models.Post.id == id) #Console output SELECT posts.id AS posts_id, posts.title AS posts_title, posts.content AS posts_content, posts.published AS posts_published, posts.created_at AS posts_created_at FROM posts WHERE posts.id = %(id_1)s
    post = post_query.first()
    if post == None:
         raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"post with id: {id} doesn't exist")
    if current_user.id != post.owner_id: #Makes sure that the owner of the post is the same who is logged in                                                       
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail=f"User: {current_user.email} authenticated but unauthorized to perform this operation")
    post_query.delete(synchronize_session=False)
    db.commit()

#working with array in local memory        
    #index = find_index_post(id) (first intent) 
    #if index == None:
    # if index == None:
    #     raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)
    #my_posts.pop(index)
    
    return Response(status_code=status.HTTP_204_NO_CONTENT) #Restful HTTP Status 204 (No Content) MUST NOT include a message body

@router.put("/{id}", response_model=schemas.Post)
def update_post(id: int, update_post: schemas.PostCreate, db: Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user)):
#---working with raw sql and the psycopg2 database driver---       
    # cursor.execute("""UPDATE posts SET title = %s, content = %s, published = %s WHERE id = %s RETURNING *""", (post.title, post.content, post.published, str(id)))
    # updated_post = cursor.fetchone()
    # conn.commit()
    # if updated_post == None: 
    #     raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)
    # return {"message" : updated_post}

#working with sqlalchemy ORM
    post_query = db.query(models.Post).filter(models.Post.id == id)  
    post = post_query.first()    
    if post == None:  
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail = f"post with the id: {id} cannot be found")
    if post.owner_id != current_user.id:  #Makes sure that the owner of the post is the same who is currently logged in 
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail=f"User: {current_user.email} authenticated but unauthorized to perform this operation")
    post_query.update(update_post.dict(), synchronize_session=False)
    db.commit()
    return post_query.first()   

#working with array in local memory    
    #index = find_index_post(id)
    #if index == None: #if not index - - works but there was an issue handlilng the zero index of the list my_posts[] 
    #post_dict = post.dict()
    #post_dict['id'] = id
    #my_posts[index] = post_dict
    #return {"message" : post_dict}








