from datetime import datetime, timedelta
from typing import Optional
from jose import JWTError, jwt
from passlib.context import CryptContext
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer

# Assessment Item 1: Database Design & Implementation (User Authentication and Token Management)
# Module: CMP2812 Full Stack Development
# By Jack Stiller, 25788983

SECRET_KEY = "NYS_PATROL_HIGH_SECURITY_SECRET_99"
ALGORITHM = "HS256"  # Commonly used algorithm for JWTs
ACCESS_TOKEN_EXPIRE_MINUTES = 30

# Plan to use Bcrypt for password hashing in future
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

# --- Password Utilities (for future implementation)---


def verify_password(plain_password, hashed_password):
    """Checks if the login password matches the hashed version in DB"""
    return pwd_context.verify(plain_password, hashed_password)


def get_password_hash(password):
    """Hashes a password before saving to the Officer table"""
    return pwd_context.hash(password)

# --- Token Utilities ---


def create_access_token(data: dict, expires_delta: Optional[timedelta] = None):
    """Generates the JWT with an expiry "exp" claim """
    to_encode = data.copy()
    expire = datetime.utcnow() + (expires_delta or timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES))
    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)

# --- Security ---


async def get_current_user(token: str = Depends(oauth2_scheme)):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username = payload.get("sub")

        # Check if entry is missing
        if username is None:
            raise credentials_exception

        # Only if it's a string it is returned
        return str(username)

    except JWTError:
        raise credentials_exception
