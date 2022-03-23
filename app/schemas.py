from typing import Optional
from pydantic import BaseModel, EmailStr
from datetime import datetime

# Pydantic Models for SCHEMAS for requests/responds

# REQUESTS SECHEMAS ##############################
# BASE SCHEMA
class PostBase(BaseModel):
    title: str
    content: str
    published: bool = True


# EXTENSIONS TO BASE SCHEMA:

# SCHEMA for creating posts
class PostCreate(PostBase):
    pass


########################################
# SCHEMA for creating users
class UserCreate(BaseModel):
    email: EmailStr
    password: str


class UserLogin(BaseModel):
    email: EmailStr
    password: str


########################################
# SCHEMA for access token
class Token(BaseModel):
    access_token: str
    token_type: str

class TokenData(BaseModel):
    id: Optional[str] = None




# RESPONSE SCHEMAS ##############################

# RESPONSE SCHEMA FOR USER CREATE #############
class UserOut(BaseModel):
    id: int
    email: EmailStr
    created_at: datetime

    # Tell pydantic to read data even if it isn't dictionary
    # Convert SQL Alchemy model to pydantic model
    class Config:
        orm_mode = True


# RESPONSE SCHEMA FOR POST RETURNING ###########
class Post(PostBase):
    id: int
    created_at: datetime
    owner_id: int
    # This returns details about the owner of the post
    # It returns the UserOut class, inside a variable in the Post clas. Nifty!
    owner: UserOut

    # Tell pydantic to read data even if it isn't dictionary
    # Convert SQL Alchemy model to pydantic model
    class Config:
        orm_mode = True