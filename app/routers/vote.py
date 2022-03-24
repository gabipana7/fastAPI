from fastapi import Body, FastAPI, Response, status, HTTPException, Depends, APIRouter
from sqlalchemy.orm import Session

# Script we created imports (.. means one folder up)
from ..database import get_db
from .. import models, schemas, database, utils, oauth2

# Create router instead of app
router = APIRouter(
    # Use a prefix to set the default routes path 
    prefix="/votes",
    tags=['Votes']
)


@router.post("/", status_code=status.HTTP_201_CREATED)
def vote(vote: schemas.Vote, db: Session = Depends(database.get_db), 
        current_user: int = Depends(oauth2.get_current_user)):

    # IF THE POST DOESN'T EXIST
    # check if user wants to vote on post that doesn't exist
    post = db.query(models.Post).filter(models.Post.id == vote.post_id).first()

    # doesn't matter the direction, any action on inexisting post should return a 404
    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail =f"Post with id {vote.post_id} does not exist")


    # IF THE POST EXISTS
    # query to see if the vote already exists
    # filter by two checks: 
    # post_id exist in vote and inputed post , user_id exists in vote and user trying to vote
    vote_query = db.query(models.Vote).filter(models.Vote.post_id == vote.post_id, 
                                    models.Vote.user_id == current_user.id)
    
    # choose the first found vote 
    found_vote = vote_query.first()
    
    # Check the direction of the voting schema
    # If direction = 1 user wants to like the post
    if (vote.dir == 1):
        # If the vote already exist raise exception
        if found_vote:
            raise HTTPException(status_code=status.HTTP_409_CONFLICT,
                                detail=f"user {current_user.id} has already voted on post {vote.post_id}")
    
        # If the vote does not exist, create the new vote
        new_vote = models.Vote(post_id = vote.post_id, user_id = current_user.id)

        # Add and commit to DB
        db.add(new_vote)
        db.commit()
        return {"message": "succesfuly added vote"}

    # If direction = 0 user wants to remove the like
    else:
        # If there is no vote for the post the user chose raise exception
        if not found_vote:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                                detail="Vote does not exists")
       
        # If vote exists, delete the vote query and commit
        vote_query.delete(synchronize_session=False)
        db.commit()

        return {"message": "succesfuly deleted vote"}