
from core.hashing import Hasher

"""
DB Model imports
"""
from db.models.user import User 

"""
DB Schema imports
"""
from schemas.user import UserListResponse,UserResponseItem,UserDetailResponse,UserUpdateRequest,UserCreate

"""
SQLalchemy imports
"""
from sqlalchemy.orm import Session

"""
Other python imports
"""

import uuid
from dotenv import load_dotenv
import uuid
from typing import *
from utils.logging_config import logger


load_dotenv()

def user_register(user: UserCreate, db: Session):
    logger.info(f"Registering user with email: {user.email}")
    try:
        existing_user = db.query(User).filter(User.email == user.email).first()
        
        if existing_user:
            logger.warning(f"User with email {user.email} already exists.")
            return False, f"No Email found - {user.email}"
        
        hashed_password = Hasher.get_password_hash(user.password)
        
        new_user = User(
            fullname=user.fullname, 
            email=user.email, 
            password=hashed_password,
            address=user.address,
            secret_key=str(uuid.uuid4()),
        )
        db.add(new_user)
        db.commit()
        db.refresh(new_user)

        user_info = {"email": new_user.email, "secret_key": new_user.secret_key}
        logger.info(f"User registered successfully: {new_user.email}")
        return True, user_info

    except Exception as e:
        logger.error(f"Error during user registration: {e}")
        return False, f"Error occurred: {e}"


def get_users(page, limit, search: Optional[str], db: Session) -> Tuple[bool, Union[UserListResponse, str]]:
    logger.info(f"Fetching users, page: {page}, limit: {limit}, search: {search}")
    try:
        query = db.query(User).filter(User.is_delete == False, User.is_active == True)

        if search:
            search_like = f"%{search}%"
            query = query.filter(
                or_(
                    User.email.ilike(search_like),
                    User.fullname.ilike(search_like)
                )
            )

        query = query.offset((page - 1) * limit).limit(limit)
        users = query.all()

        user_list = [
            UserResponseItem(
                id=user.id,
                fullname=user.fullname,
                email=user.email
            )
            for user in users
        ]

        if user_list:
            logger.info(f"{len(user_list)} users found")
            return True, UserListResponse(data=user_list)
        else:
            logger.info("No users found")
            return False, "No data found"

    except Exception as e:
        logger.error(f"Error fetching users: {e}")
        return False, f"Error occurred: {e}"


def get_user_by_id(user_id, db: Session) -> Tuple[bool, Union[UserDetailResponse, str]]:
    logger.info(f"Fetching user by ID: {user_id}")
    try:
        user = db.query(User).filter(User.id == user_id, User.is_delete == False, User.is_active == True).first()

        if user:
            user_detail = UserDetailResponse(
                id=user.id,
                fullname=user.fullname,
                email=user.email,
                phone=user.phone,
                address=user.address
            )
            logger.info(f"User found: {user.fullname}")
            return True, user_detail
        else:
            logger.warning(f"User with ID {user_id} not found")
            return False, "User not found"

    except Exception as e:
        logger.error(f"Error fetching user by ID {user_id}: {e}")
        return False, f"Error occurred: {e}"


def update_user(id: int, update_data: UserUpdateRequest, db: Session):
    logger.info(f"Updating user ID: {id}")
    try:
        user = db.query(User).filter(User.id == id, User.is_delete == False, User.is_active == True).first()

        if not user:
            logger.warning(f"User with ID {id} not found for update")
            return False, "user not found"

        for field, value in update_data.dict(exclude_unset=True).items():
            setattr(user, field, value)

        db.commit()
        logger.info(f"User updated: {user.fullname}")
        return True, f"User updated successfully: {user.fullname}"

    except Exception as e:
        logger.error(f"Error updating user ID {id}: {e}")
        return False, f"{e}"


def delete_user(id: int, db: Session):
    logger.info(f"Toggling delete status for user ID: {id}")
    try:
        user = db.query(User).filter(User.is_active == True, User.id == id).first()

        if not user:
            logger.warning(f"User with ID {id} not found for delete toggle")
            return False, "user not found"

        user.is_delete = not user.is_delete
        db.commit()
        logger.info(f"User delete status updated: {user.fullname}, is_delete={user.is_delete}")
        return True, f"User deleted successfully: {user.fullname}, status: {user.is_delete}"

    except Exception as e:
        logger.error(f"Error deleting user ID {id}: {e}")
        return False, f"{e}"
