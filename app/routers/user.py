from fastapi import Body, FastAPI, Response, status, HTTPException, Depends, APIRouter
from sqlalchemy.orm import Session

# Script we created imports (.. means one folder up)
from ..database import get_db
from .. import models,schemas,utils

# Create router instead of app
router = APIRouter(
    # Use a prefix to set the default routes path 
    prefix="/users",
    tags=['Users']
)


######################################## USERS ########################################
# CREATE USER #########################################
@router.post("/", status_code=status.HTTP_201_CREATED, response_model=schemas.UserOut)
def create_users(user: schemas.UserCreate, db: Session = Depends(get_db)):

    # Hash the password - user.password
    hashed_password = utils.hash(user.password)
    # Update the pydantic user model password with the hashed password
    user.password = hashed_password

    new_user = models.User(**user.dict())
    # Add to database
    db.add(new_user)
    # Commit changes
    db.commit()
    # Retrieve post and store into new variable
    db.refresh(new_user)

    return new_user


# RETRIEVE USER INFO BASED ON ID #########################################
@router.get('/{id}', response_model=schemas.UserOut)
def get_user(id: int,db: Session = Depends(get_db)):
    user = db.query(models.User).filter(models.User.id == id).first()

    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"user with id {id} does not exist") 

    return user