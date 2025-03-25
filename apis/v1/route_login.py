from core.config import settings
from core.hashing import Hasher
from core.security import create_access_token
from db.repository.login import get_user
from db.session import get_db
from fastapi import APIRouter
from fastapi import Depends,HTTPException, status, Header
from fastapi import HTTPException
from fastapi import status
from fastapi.security import OAuth2PasswordBearer
from fastapi.security import OAuth2PasswordRequestForm
from jose import jwt
from jose import JWTError
from schemas.token import Token
from sqlalchemy.orm import Session
from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials

security = HTTPBearer()

router = APIRouter()



def get_auth_current_user(credentials: HTTPAuthorizationCredentials = Depends(security)):
    token = credentials.credentials
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM])
        email: str = payload.get("email")
        secret: str = payload.get("secret_key")
        id: str = payload.get("user_id")
        print(f"Debug: Decoded payload: {payload}")
        print(f"Debug: Email: {email}")
        print(f"Debug: _id: {id}")
        

        if not email:
            raise credentials_exception

        return {"email": email, "secret": secret,"user_id":id}
    except JWTError as e:
        print(f"❌ Debug: JWT Error: {str(e)}")
        raise credentials_exception


def get_auth_admin(authorization: str = Header(..., convert_underscores=False)):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        scheme, token = authorization.split(" ")
        if scheme.lower() != "bearer":
            raise credentials_exception
        payload = jwt.decode(token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM])
        email: str = payload.get("email")
        if email is None:
            raise credentials_exception
        return {"email":email}
    except JWTError:
        print("---errror")
        raise credentials_exception