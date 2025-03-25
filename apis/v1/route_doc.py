"""
Fast api imports
"""
from fastapi import APIRouter,File,UploadFile
from fastapi import Depends,status
from fastapi.security import OAuth2PasswordBearer
from fastapi.openapi.models import OAuthFlows as OAuthFlowsModel

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

"""
DB Repository imports
"""
from db.repository.user_doc import upload_file,list_filename,query_rag

"""
DB Schema imports
"""
from utils.permissions import *
from utils.logging_config import logger

"""
Other python imports
"""
import os

"""
Other router imports
"""
from apis.v1.route_login import get_auth_current_user

base_url=os.getenv("BASEURL")
router = APIRouter()


from fastapi import  Depends,  status
from fastapi.security import OAuth2PasswordBearer


oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

"""
Register api for user registeration
"""

@router.post("/documents/")
async def document_upload(file: UploadFile = File(...), current_user: dict = Depends(get_auth_current_user)):
    try:
        logger.info(f"Document upload request from user: {current_user}")
        current_user = current_user["user_id"]

        data = await upload_file(file, current_user)

        if data[0] is False:
            logger.warning(f"Upload failed: {data[1]}")
            return {
                "data": [],
                "message": data[1],
                "status_code": status.HTTP_400_BAD_REQUEST
            }

        logger.info("Document uploaded successfully")
        return {
            "data": [data[1]],
            "message": "User created successfully",
            "status_code": status.HTTP_201_CREATED
        }

    except Exception as e:
        logger.error(f"Exception in document_upload: {e}")
        return {
            "data": str(e),
            "message": "Email not found",
            "status_code": status.HTTP_400_BAD_REQUEST
        }


@router.get("/documents/")
async def document_list(current_user: dict = Depends(get_auth_current_user)):
    try:
        logger.info(f"Document list requested by user: {current_user['user_id']}")
        data = await list_filename()

        logger.debug(f"Total documents fetched: {len(data)}")

        if data[0] is False:
            logger.warning(f"Document list fetch failed: {data[1]}")
            return {
                "data": [],
                "message": data[1],
                "status_code": status.HTTP_400_BAD_REQUEST
            }

        logger.info("Document list fetched successfully")
        return {
            "data": [data[1]],
            "message": "Answer viewed successfully",
            "status_code": status.HTTP_201_CREATED
        }

    except Exception as e:
        logger.error(f"Exception in document_list: {e}")
        return {
            "data": str(e),
            "message": "Email not found",
            "status_code": status.HTTP_400_BAD_REQUEST
        }


@router.post("/query/")
async def document_list(query: str, filename: str, current_user: dict = Depends(get_auth_current_user)):
    try:
        logger.info(f"Query received: '{query}' on file '{filename}' by user {current_user['user_id']}")
        current_user = current_user["user_id"]

        data = await query_rag(query, current_user, filename)

        if data[0] is False:
            logger.warning(f"Query failed: {data[1]}")
            return {
                "data": [],
                "message": data[1],
                "status_code": status.HTTP_400_BAD_REQUEST
            }

        logger.info("Query processed successfully")
        return {
            "data": [data[1]],
            "message": "User created successfully",
            "status_code": status.HTTP_201_CREATED
        }

    except Exception as e:
        logger.error(f"Exception in query: {e}")
        return {
            "data": str(e),
            "message": "Email not found",
            "status_code": status.HTTP_400_BAD_REQUEST
        }