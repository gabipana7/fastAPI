from fastapi import FastAPI
from sqlalchemy.orm import Session


# Script we created imports
from . import models
from .database import engine, SessionLocal

# Import routers
from .routers import post, user, auth, vote

# Import validation for environment variables
from .config import settings



print(settings.database_username)

# NO LONGER NEEDED BECAUSE OF ALEMBIC

# # Implement models (from models.py) and create dqlalchemy engine (from database.py)
# models.Base.metadata.create_all(bind=engine)

# Alembic migration config in alembic.ini and env.py in alembic folder




# Implement application
app = FastAPI()


# Include the post and user routers 
app.include_router(post.router)
app.include_router(user.router)
app.include_router(auth.router)
app.include_router(vote.router)


@app.get("/")
def root():
    return {"message": "Hello World"}






