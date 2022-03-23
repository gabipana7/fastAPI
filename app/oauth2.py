from jose import JWTError, jwt
from datetime import datetime, timedelta
from . import schemas, database, models
from fastapi import Depends, status, HTTPException
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session

oauth2_scheme = OAuth2PasswordBearer(tokenUrl='/login')

# Import Environment Variables
from .config import settings

# SECRET_KEY
# to get a string like this run:
# openssl rand -hex 32
SECRET_KEY = settings.secret_key

# ALGORITHM
ALGORITHM = settings.algorithm

# EXPIRATION TIME FOR TOKEN 
ACCESS_TOKEN_EXPIRE_MINUTES = settings.access_token_expire_minutes


# Creation of access token when loging in
def create_access_token(data: dict):
    to_encode = data.copy()

    expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})

    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)

    return encoded_jwt


# Verification of previously assigned token and extraction of token data (id here)
def verify_access_token(token: str, credentials_exception):

    try:
        # Stores the data
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])

        #  Extract data
        id: str =payload.get("user_id")

        # Check if id exists or not 
        if id is None:
            raise credentials_exception

        # Token data, for now it is just the id
        token_data = schemas.TokenData(id=id)
    
    except JWTError:
        raise credentials_exception

    # Return the token data (just an id here)
    return token_data


# Pass it as a dependency in any path operation
# takes the token from the request, verifies it, extracts id and auto fetch the user from DB 
def get_current_user(token: str = Depends(oauth2_scheme), db: Session = Depends(database.get_db)):

    credentials_exception = HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                                            detail = f"Could not validate credentials", 
                                            headers={"WWW-Authenticate": "Bearer"})

    # Selects the token and verifies it
    token = verify_access_token(token, credentials_exception)

    # Extracts user from database based on id from token
    user = db.query(models.User).filter(models.User.id == token.id).first()

    # Return the user 
    return user