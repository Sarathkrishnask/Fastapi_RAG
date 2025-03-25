"""
Fast api imports
"""
from fastapi import APIRouter
from fastapi import Depends,status
from fastapi.security import OAuth2PasswordBearer
from fastapi.openapi.models import OAuthFlows as OAuthFlowsModel

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

"""
SQLalchemy imports
"""
from sqlalchemy.orm import Session
from sqlalchemy import text

"""
DB Model imports
"""
from db.session import get_db

"""
DB Repository imports
"""
from db.repository.user import (
    user_register,get_users,get_user_by_id,update_user,delete_user
)

"""
DB Schema imports
"""
from schemas.user import UserCreate,UserUpdateRequest
from utils.logging_config import logger

"""
Other python imports
"""
import os


base_url=os.getenv("BASEURL")
router = APIRouter()


from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer


oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

"""
Register api for user registeration
"""

@router.post("/createuser")
def createuser(user: UserCreate, db: Session = Depends(get_db)):
    try:
        logger.info("User registration requested")
        data = user_register(user, db)
        if data[0] == False:
            logger.warning(f"User creation failed: {data[1]}")
            return {"data": [], "message": data[1], "status_code": status.HTTP_400_BAD_REQUEST}
        elif data[0] == True:
            logger.info("User created successfully")
            return {"data": [data[1]], "message": "User created successfully", "status_code": status.HTTP_201_CREATED}
    except Exception as e:
        logger.error(f"Exception in createuser: {e}")
        return {"data": str(e), "message": "Email not found", "status_code": status.HTTP_400_BAD_REQUEST}


@router.get("/user_list")
def user_list(page: int = 1, limit: int = 10, search: str = None, db: Session = Depends(get_db)):
    try:
        logger.info(f"User list requested - Page: {page}, Limit: {limit}, Search: {search}")
        data = get_users(page, limit, search, db)
        if data[0] == False:
            logger.warning(f"Fetching user list failed: {data[1]}")
            return {"data": [], "message": data[1], "status_code": status.HTTP_400_BAD_REQUEST}
        elif data[0] == True:
            if data[0] == None:
                logger.info("User list returned: No content")
                return {"data": [data[1]], "message": "No content to show", "status_code": status.HTTP_204_NO_CONTENT}
            else:
                logger.info("User list fetched successfully")
                return {"data": [data[1]], "message": "User viewed successfully", "status_code": status.HTTP_200_OK}
    except Exception as e:
        logger.error(f"Exception in user_list: {e}")
        return {"data": str(e), "message": "Error", "status_code": status.HTTP_400_BAD_REQUEST}


@router.get("/users/{user_id}")
def users_by_id(user_id: int, db: Session = Depends(get_db)):
    try:
        logger.info(f"Fetching user by ID: {user_id}")
        data = get_user_by_id(user_id, db)
        if data[0] == False:
            logger.warning(f"User fetch failed: {data[1]}")
            return {"data": [], "message": data[1], "status_code": status.HTTP_400_BAD_REQUEST}
        elif data[0] == True:
            logger.info("User fetched successfully by ID")
            return {"data": [data[1]], "message": "User viewed successfully", "status_code": status.HTTP_200_OK}
    except Exception as e:
        logger.error(f"Exception in users_by_id: {e}")
        return {"data": str(e), "message": "errro while get records", "status_code": status.HTTP_400_BAD_REQUEST}


@router.patch("/users/{user_id}")
def user_update(user_id: int, update_data: UserUpdateRequest, db: Session = Depends(get_db)):
    try:
        logger.info(f"Updating user ID: {user_id}")
        data = update_user(user_id, update_data, db)
        if data[0] == False:
            logger.warning(f"User update failed: {data[1]}")
            return {"data": [], "message": data[1], "status_code": status.HTTP_400_BAD_REQUEST}
        elif data[0] == True:
            logger.info("User updated successfully")
            return {"data": [data[1]], "message": "User viewed successfully", "status_code": status.HTTP_200_OK}
    except Exception as e:
        logger.error(f"Exception in user_update: {e}")
        return {"data": str(e), "message": "error while update", "status_code": status.HTTP_400_BAD_REQUEST}


@router.delete("/users/{user_id}")
def user_delete(user_id: int, db: Session = Depends(get_db)):
    try:
        logger.info(f"Deleting user ID: {user_id}")
        data = delete_user(user_id, db)
        if data[0] == False:
            logger.warning(f"User deletion failed: {data[1]}")
            return {"data": [], "message": data[1], "status_code": status.HTTP_400_BAD_REQUEST}
        elif data[0] == True:
            logger.info("User deleted successfully")
            return {"data": [data[1]], "message": "User deleted successfully", "status_code": status.HTTP_200_OK}
    except Exception as e:
        logger.error(f"Exception in user_delete: {e}")
        return {"data": str(e), "message": "error while delete", "status_code": status.HTTP_400_BAD_REQUEST}


@router.get("/health-check")
def health_check(db: Session = Depends(get_db)):
    try:
        logger.debug("Performing DB health check")
        db.execute(text("SELECT 1"))
        logger.info("DB connection is healthy")
        return {"status": "ok", "message": "DB connection is healthy"}
    except Exception as e:
        logger.error(f"DB health check failed: {e}")
        raise HTTPException(status_code=503, detail=f"DB issue: {str(e)}")