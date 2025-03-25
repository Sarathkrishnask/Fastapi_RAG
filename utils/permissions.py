from fastapi import Depends, HTTPException, status, Request
from jose import jwt, JWTError
from typing import List
from fastapi import Header
from apis.v1.route_login import get_auth_current_user
from sqlalchemy.orm import Session

from fastapi import Depends, HTTPException, Request
from sqlalchemy.orm import Session
from db.session import engine, get_db



from fastapi import Depends, HTTPException, Request
from sqlalchemy.orm import Session

from db.session import engine, get_db

class PermissionAll:
    def __call__(self, current_user: dict = Depends(get_auth_current_user)):
        roles = current_user.get("user_id", [])
        print(roles,"----roles")

        return roles
