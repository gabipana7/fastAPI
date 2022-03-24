from fastapi import FastAPI
# CORS Import
from fastapi.middleware.cors import CORSMiddleware

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

#origins = ["https://www.google.com","https://www.google.ro"]
# Every single origin:
origins =["*"]


# CORS implementation in order to be able to receive requests from browser NOT on our domain
# By default we can only receive requests from browser hosted on the same domain as app
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)



# Include the post and user routers 
app.include_router(post.router)
app.include_router(user.router)
app.include_router(auth.router)
app.include_router(vote.router)


# Default get request (home page)
@app.get("/")
def root():
    return {"message": "Hello World"}






