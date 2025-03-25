"""
CORE imports
"""
from core.hashing import Hasher
from core.config import settings

"""
DB Model imports
"""
from db.models.user import User

"""
DB Schema imports
"""
from schemas.user import  Userlogin
"""
SQLalchemy imports
"""
from sqlalchemy import or_, and_,select
from sqlalchemy.orm import Session


"""
UTIls import
"""
from utils.functions import create_reset_token

"""
Other python imports
"""
import os
from jose import jwt ,JWTError
from sqlalchemy.ext.asyncio import AsyncSession

from dotenv import load_dotenv
from typing import *
import logging


load_dotenv()

logger = logging.getLogger(__name__)


def userlogin(user: Userlogin, db: AsyncSession):
    try:
        result =  db.execute(
            select(User).where(User.email == user.email)
        )
        existing_user = result.scalar_one_or_none()

        if not existing_user:
            logger.warning(f"Login attempt for non-existent email: {user.email}")
            return False, f"Given email not exists - {user.email}"

        check_password = Hasher.verify_password(user.password, existing_user.password)
        if not check_password:
            logger.warning(f"Incorrect password attempt for email: {user.email}")
            return False, f"Given password is incorrect - {user.email}"

        user_info = {
            "email": existing_user.email,
            "secret_key": existing_user.secret_key,
            "user_id":str(existing_user.id)
        }
        return True, user_info

    except Exception as e:
        logger.error(f"Error in userlogin: {str(e)}")
        return False, f"An error occurred during login: {str(e)}"


def verify_refresh_token(refresh_token: str) -> Dict[str, Any]:
    try:
        # Decode the token using the secret key and algorithm
        payload = jwt.decode(refresh_token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM])
        
        return True ,payload  # Return the payload if verification is successful

    except jwt.ExpiredSignatureError:
        return False,"Refresh token has expired"
    except jwt.PyJWTError:
        return False,"Invalid refresh token"

def forget_passwd(usr_data,db):
    try:
        print(usr_data)
        user = db.query(User).filter(User.email == usr_data.email).first()
        if not user:
            return False,"Usersss not found"

        # Create a reset token
        reset_token = create_reset_token(user.email)
        user_data = {"email":user.email, "Token":reset_token}
        # reset_pwd = f"http://127.0.0.1:8000/auth/reset-password/{reset_token}"
        try:
            logger.debug(f"Attempting to send Forgot password email to  {user.email}")
            # asyncio.run(send_forgot_email(user.email, reset_token))
            logger.info(f"Forgot passwor email sent successfully to {user.email}")
        except Exception as e:
            logger.error(f"Failed to send Forgot passwor email: {str(e)}")
            return False, "Failed to send Forgot passwor email. Please try again later."
        return True , user_data
    except Exception as e:
        return False, f"Error Occured {e}"


def verify_reset_token(token: str, db: Session):
    try:
        payload = jwt.decode(token, os.getenv("SECRET_KEY"), algorithms=["HS256"])
        email: str = payload.get("sub")

        if email is None:
            logger.warning("Reset token payload does not contain email (sub).")
            return False, "Invalid token"

        user = db.query(User).filter(User.email == email).first()
        if not user:
            logger.warning(f"No user found for email extracted from token: {email}")
            return False, "User not found"

        logger.info(f"Reset token successfully verified for email: {email}")
        return user

    except JWTError as e:
        logger.error(f"JWT error while verifying reset token: {str(e)}")
        return False, "Invalid token"
    
def change_passwd(usr_data, db):
    try:
        logger.debug("Verifying reset token for password change.")
        user_info = verify_reset_token(usr_data.token, db)

        if not user_info or isinstance(user_info, tuple):
            logger.warning("Token verification failed during password change.")
            return user_info  # Either False, "Invalid token" or similar

        logger.debug(f"Token verified. Updating password for user: {user_info.email}")

        if usr_data.password == usr_data.confirm_password:
            logger.debug("Password and confirm password matched.")
            hashed_password = Hasher.get_password_hash(usr_data.password)
            logger.debug("Password hashed successfully.")
            user_info.password = hashed_password
        else:
            logger.warning(f"Password mismatch: {usr_data}")
            return False, "Password and Confirm password not match"

        db.commit()
        logger.info(f"Password reset successfully for user: {user_info.email}")
        return True, f"Password reset successfully : {user_info.email}"

    except Exception as e:
        logger.error(f"Error occurred while changing password: {str(e)}")
        return False, f"Error Occurred: {str(e)}"
