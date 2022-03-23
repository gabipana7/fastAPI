# This file stores a bunch of UTILITY files
from pydoc import plain
from passlib.context import CryptContext

# Hashing algorithm used
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# Define function that hashes
def hash(password: str):
    return pwd_context.hash(password)


# Password verified - introduced by user VS pass from database
def verify(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)