from fastapi import Body, FastAPI, Response, status, HTTPException, Depends, APIRouter
from sqlalchemy.orm import Session
from typing import  List, Optional

# Script we created imports (.. means one folder up)
from ..database import get_db
from .. import models, schemas, utils, oauth2

# Create router instead of app

router = APIRouter(
    # Use a prefix to set the default routes path 
    prefix="/posts",
    tags=['Posts']
)


######################################## POSTS ########################################
# CREATE #########################################
@router.post("/", status_code=status.HTTP_201_CREATED, response_model=schemas.Post)
def create_posts(post: schemas.PostCreate, db: Session = Depends(get_db), 
                        current_user: int = Depends(oauth2.get_current_user)):
    # # SQL   
    # # SQL Injection: when someone tries to insert SQL queries as values in DB 
    # # sequel injection risk, DO NOT do it like this:
    # #cursor.execute("""INSERT INTO posts (title, content, published) VALUES 
    # #                ({post.title}, {post.content}, {post.published})""")

    # # use placeholders %s instead:
    # cursor.execute("""INSERT INTO posts (title, content, published) VALUES (%s, %s, %s)
    #                 RETURNING *""",(post.title, post.content, post.published))

    # new_post = cursor.fetchone()

    # # This alone does not push the changes to the DB. You have to ref the connection:
    # # Commit changes to the connection to the DB
    # conn.commit()

    # print(current_user.id)
    # print(current_user.email)
    # ORM
    # NEW post structure
   
    #new_post = models.Post(title=post.title, content=post.content, published=post.published)
    # Or use ** to unpack the fields in the post model
    new_post = models.Post(owner_id=current_user.id, **post.dict())

    # Add to database
    db.add(new_post)

    # Commit changes
    db.commit()

    # Retrieve post and store into new variable
    db.refresh(new_post)
    return new_post



# READ #########################################
@router.get("/", response_model=List[schemas.Post])
def get_posts(db: Session = Depends(get_db),
                # Get current user, use oauth2 to check for token!
                current_user: int = Depends(oauth2.get_current_user),
                # Use query parameters, ex: to limit of posts to get
                limit: int = 10,
                skip: int = 0,
                search: Optional[str] = ""):
    # SQL
    # cursor.execute("""SELECT * FROM posts""")
    # posts = cursor.fetchall()

    # ORM ( INCLUDES SQL SYNTAX INSIDE)
    posts = db.query(models.Post).filter(models.Post.title.contains(search)).limit(limit).offset(skip).all()

    # If you want to filter and get just the logged in user posts. 
    # So check posts user_id against current user id
    #posts = db.query(models.Post).filter(models.Post.owner_id == current_user.id).all()
    return posts



# READ ID #########################################
@router.get("/{id}", response_model=schemas.Post)
# Implement validation with (id: int) <- force convert to int in request
def get_post(id: int, db: Session = Depends(get_db), 
                current_user: int = Depends(oauth2.get_current_user)):
    # # SQL    
    # # Select post based on id
    # cursor.execute("""SELECT * FROM posts WHERE id = %s""", (str(id),))
    # # Fetch
    # post = cursor.fetchone()

    # ORM
    post = db.query(models.Post).filter(models.Post.id == id).first()

    # If post does not exist
    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, 
                            detail=f"post with id {id} was not found")

    # If you want to filter and be able to get just the logged in user post. 
    # So check post user_id against current user id
    # Check if the owner of the post is trying to view his posts:
    #if post.owner_id != current_user.id:
    #    raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,
    #                        detail="Not authorized to perform requested action")

    return post



# DELETE #########################################
@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_post(id: int, db: Session = Depends(get_db), 
                        current_user: int = Depends(oauth2.get_current_user)):
    # # SQL    
    # # Cursor command that executes the delete
    # cursor.execute("""DELETE FROM posts WHERE id = %s RETURNING * """,(str(id),))

    # # Fetch the deleted post
    # deleted_post = cursor.fetchone()

    # # Commit the changes
    # conn.commit()

    # ORM
    # Save the query based on id
    post_query = db.query(models.Post).filter(models.Post.id == id)
    post = post_query.first()

    # If post does not exist
    if post == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"post with id {id} does not exist")

    # Check if the owner of the post is trying to delete his post
    if post.owner_id != current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,
                            detail="Not authorized to perform requested action")

    # Delete post
    post_query.delete(synchronize_session=False)
    # Commit changes
    db.commit()

    return Response(status_code=status.HTTP_204_NO_CONTENT)



# UPDATE #########################################
@router.put("/{id}", response_model=schemas.Post)
def update_post(id: int, updated_post: schemas.PostCreate,  db: Session = Depends(get_db), 
                        current_user: int = Depends(oauth2.get_current_user)):
    # # SQL
    # # Cursor command that executes the update
    # cursor.execute("""UPDATE posts SET title = %s, content = %s, published = %s 
    #                 WHERE ID = %s RETURNING *""", 
    #                 (post.title, post.content, post.published, str(id))) 
    
    # # Fetch the updated post
    # updated_post = cursor.fetchone()

    # # Commit the changes
    # conn.commit()

    # ORM
    # Save the query based on id
    post_query = db.query(models.Post).filter(models.Post.id == id)

    # Grab that specifit post
    post = post_query.first()

    # If post does not exist
    if post == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"post with id {id} does not exist")

    # Check if the owner of the post is trying to update his post
    if post.owner_id != current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,
                            detail="Not authorized to perform requested action")
    
    # If exists
    # Chain an update method to the query saved earlier
    # Pass the fields you want to update as a dictionary (from post schema)
    post_query.update(updated_post.dict(), synchronize_session=False)

    # Commit changes
    db.commit()                

    return post_query.first()