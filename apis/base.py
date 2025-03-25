# from apis.v1 import route_login
from sys import prefix
from apis.v1 import (
    route_user,route_login,
    route_validation,route_doc)
from fastapi import APIRouter


api_router = APIRouter()

api_router.include_router(route_validation.router, prefix="", tags=["validation"])
api_router.include_router(route_user.router, prefix="", tags=["users"])
api_router.include_router(route_doc.router, prefix="", tags=["documents"])
api_router.include_router(route_login.router, prefix="", tags=["user_login"])


