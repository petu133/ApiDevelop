from fastapi import Response, status, HTTPException, Depends, APIRouter
from sqlalchemy.orm import Session
from .. import models, schemas, utils
from ..database import get_db

router = APIRouter(   #router object allows to split up different path operation into distinc files    
    prefix="/users",
    tags=['Users'] #groups the paths by sections inside the auto-generated Swagger UI documentation
    )  #router object allows to split up different path operation into distinc files

@router.post("/", status_code=status.HTTP_201_CREATED, response_model=schemas.UserOut)
def create_user(user: schemas.UserCreate, db: Session = Depends(get_db)):
#user pydantic object should be of type UserCreate (class in Schemas.py) | Add a colon and a data type after each function parameter 
#| Add a colon and a data type after each function parameter websource --- https://towardsdatascience.com/type-hints-in-python-everything-you-need-to-know-in-5-minutes-24e0bad06d0b ---
    
    #hash the password - user.password (obtained from the pydantic model)
    hashed_password = utils.hash(user.password)
    user.password = hashed_password
    new_user = models.User(**user.dict())
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user

@router.get('/{id}', response_model=schemas.UserOut)
def get_user(id: int, db: Session = Depends(get_db)):
    user = db.query(models.User).filter(models.User.id == id).first() 
#there should be only one id for each user, therefore is advisable grab the first occurrence
        #to avoid wasting resources looking exhaustively through the database
   
    if not user:
        raise HTTPException(status.HTTP_404_NOT_FOUND, detail=f"The user with the id: {id} not found")
    return user
   






