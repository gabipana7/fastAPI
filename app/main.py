from fastapi import FastAPI
from sqlalchemy.orm import Session


# Script we created imports
from . import models
from .database import engine, SessionLocal

# Import routers
from .routers import post, user, auth

# Import validation for environment variables
from .config import settings



print(settings.database_username)

# Implement models (from models.py) and bind to engine (from database.py)
models.Base.metadata.create_all(bind=engine)

# Implement application
app = FastAPI()


# Include the post and user routers 
app.include_router(post.router)
app.include_router(user.router)
app.include_router(auth.router)


@app.get("/")
def root():
    return {"message": "Hello World"}






