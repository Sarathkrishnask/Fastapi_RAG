"""
Fast api imports
"""
from fastapi import APIRouter
from fastapi import Depends
from fastapi import status
from fastapi.security import OAuth2PasswordBearer
from fastapi.openapi.models import OAuthFlows 

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

"""
SQLalchemy imports
"""
from sqlalchemy.orm import Session

"""
DB Model imports
"""
from db.session import get_db

"""
DB Repository imports
"""

from db.repository.validation import *


"""
DB Schema imports
"""
from schemas.user import Userlogin,ForgetPwd,ResetPasswordRequest


"""
CORE imports
"""
from core.security import create_access_token

"""
Other python imports
"""
import os


base_url=os.getenv("BASEURL")
router = APIRouter()


@router.post("/auth/login/")        
def login(user: Userlogin, db: Session = Depends(get_db)):
    try:
        data = userlogin(user, db)
        if data[0] == False:
            logger.warning(f"Login failed for user: {user.email} - Reason: {data[1]}")
            return {"data":[],"message":data[1],"status_code":status.HTTP_400_BAD_REQUEST}
        elif data[0] == True:
            logger.info(f"User logged in successfully: {user.email}")
            access_token = create_access_token(data[1])
            data_output = {"access_token":access_token, "email":data[1]["email"]}
            return {"data":data_output,"message":"login successfully","status_code":status.HTTP_200_OK}
    except Exception as e:
        logger.error(f"Exception during login: {str(e)}")
        return {"data":str(e),"message":"unable to login","status_code":status.HTTP_400_BAD_REQUEST}
    

@router.post("/auth/forgot-password")
def forgot_password(frgt_pwd:ForgetPwd,db: Session=Depends(get_db)):
    try:
        data = forget_passwd(frgt_pwd, db)
        if data[0] == False:
            logger.warning(f"Forgot password failed for: {frgt_pwd.email} - Reason: {data[1]}")
            return {"data":[],"message":data[1],"status_code":status.HTTP_400_BAD_REQUEST}
        elif data[0] == True:
            logger.info(f"Forgot password email sent to: {frgt_pwd.email}")
            return {"data":data[1],"message":"email send to you email","status_code":status.HTTP_200_OK}
    except Exception as e:
        logger.error(f"Exception in forgot password: {str(e)}")
        return {"data":str(e),"message":"error while try to send email","status_code":status.HTTP_400_BAD_REQUEST}



@router.post("/auth/reset-password")
def reset_password(rst_pwd:ResetPasswordRequest,db: Session=Depends(get_db)):
    try:
        data = change_passwd(rst_pwd, db)
        if data[0] == False:
            logger.warning(f"Reset password failed for:  - Reason: {data[1]}")
            return {"data":[],"message":data[1],"status_code":status.HTTP_400_BAD_REQUEST}
        elif data[0] == True:
            logger.info(f"Password reset successful for: {data[1]}")
            return {"data":data[1],"message":"reset password sucessfully","status_code":status.HTTP_200_OK}
    except Exception as e:
        logger.error(f"Exception in reset password: {str(e)}")
        return {"data":str(e),"message":"response_message.FAILURE_MESSAGE_EMAIL","status_code":status.HTTP_400_BAD_REQUEST}
