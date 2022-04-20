from fastapi import Response, status, HTTPException, Depends, APIRouter
from .. import schemas, database, models, oauth2
from sqlalchemy.orm import Session

router = APIRouter(prefix="/vote", tags=['Vote'])

@router.post("/", status_code=status.HTTP_201_CREATED)
def vote(vote: schemas.Vote, db: Session = Depends(database.get_db), current_user: int = Depends(oauth2.get_current_user)):
    vote_query = db.query(models.Vote).filter(models.Vote.post_id == vote.post_id, models.Vote.user_id == current_user.id )
    found_vote = vote_query.first()
    if (vote.dir == 1): # means that the user want to like a post
        if found_vote:  # the user already voted this specific post, so he cannot do it again
            raise HTTPException(status_code=status.HTTP_409_CONFLICT, 
            detail=f"The user with id: {current_user.id}, cannot vote the post ({vote.post_id}) twice")
        #Otherwise, we can proceeding
        new_vote = models.Vote(post_id = vote.post_id, user_id = current_user.id) # Preparing the insertion of new entry    
        db.add(new_vote)
        db.commit()
        return {"message" : f"vote added to the post {vote.post_id}"}
    else: #if the user provides a direction 0, that means he want to delete an existing vote.
        if not found_vote:
            raise HTTPException(status.HTTP_404_NOT_FOUND, 
            detail=f"Non-existent vote in the post {vote.post_id}, the delete operation cannot be perform")
        vote_query.delete(synchronize_session=False)
        db.commit()
        return {"message" : f"vote deleted from the post {vote.post_id}"}
        
