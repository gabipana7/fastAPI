from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

import psycopg2
from psycopg2.extras import RealDictCursor
import time

from .config import settings

# URL FOR CONNECTION TO DB
SQLALCHEMY_DATABASE_URL = f'postgresql://{settings.database_username}:{settings.database_password}@{settings.database_hostname}:{settings.database_port}/{settings.database_name}'

# Engine for connection
engine = create_engine(SQLALCHEMY_DATABASE_URL)

# Session
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Define the models which will define the tables in the DB
Base = declarative_base()


# Dependency
def get_db():
    # Session is responsible for talking with DB
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


# # No longer used, Just for documentation purposes
# # We know use SQLALchemy to connect to database, so psycopg (posgres driver) is no longe necessary
# # Keep trying to connect to DB
# while True:
#     # Connect to database
#     try:
#         # Connection
#         conn = psycopg2.connect(host='localhost', database='fastapi', 
#                                 user='postgres', password='gabi1295*', 
#                                 cursor_factory=RealDictCursor)
#         # Cursor used to perform operations
#         cursor = conn.cursor()

#         # Message that it was successful
#         print("Database connection was succesful")
#         break

#     except Exception as error:
#         print("Connecting to database failed")
#         print("Error: ", error)
#         time.sleep(2)