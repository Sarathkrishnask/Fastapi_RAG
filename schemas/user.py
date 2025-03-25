from pydantic import BaseModel 
from pydantic import EmailStr 
from pydantic import Field,constr
from typing import List,Optional

class Userlogin(BaseModel):
    email: EmailStr = "superuser@gmail.com"
    password: str = "admin@123"#Field(..., min_length=4)    

class RoleCreate(BaseModel):
    roles : str

class ShowUser(BaseModel):
    id: int
    email: EmailStr
    is_active: bool
    mode:bool
    
    model_config = {
        "from_attributes": True
    }
    # class Config:  # tells pydantic to convert even non dict obj to json
    #     orm_mode = True

class ResetPassword(BaseModel):
    password: str = Field(..., min_length=4)
    confirmpassword: str = Field(..., min_length=4)

class UserMailId(BaseModel):
    email : EmailStr = "superuser@gmail.com"

class VerifyOtpLogin(BaseModel):
    email:EmailStr
    otp_values: str = Field(..., min_length=6)
    
class TokenRefresh(BaseModel):
    refresh_token: str

class ResetPasswordRequest(BaseModel):
    token: str
    password: str  #"admin@1234"#Field(..., min_length=6)
    confirm_password: str #"admin@1234" #Field(..., min_length=6)


class ForgetPwd(BaseModel):
    email: EmailStr = "superuser@gmail.com"
    # password : str
    # confirm_password : str
class ResetPwd(BaseModel):
    email: EmailStr
    password : str
    confirm_password : str
   

# properties required during user creation
class UserCreate(BaseModel):
    email: EmailStr  
    password: str = Field(..., min_length=4)
    fullname: str 
    address: str


class UserResponseItem(BaseModel):
    id: int
    fullname: Optional[str]=None
    email: EmailStr

class UserListResponse(BaseModel):
    data: List[UserResponseItem]

class UserDetailResponse(BaseModel):
    id: int
    fullname: str
    email: EmailStr 
    address: Optional[str]
    phone: Optional[str] 


class UserDeleteRequest(BaseModel):
    fullname: Optional[str]
    email: Optional[EmailStr]
    # is_active:bool


class UserUpdateRequest(BaseModel):
    fullname: Optional[str] 
    address: Optional[str] 
    phone : Optional[str] = "8962279848"#None
    


# class UserRoleUpdate(BaseModel):
#     role_id: int
# properties required during user creation
class UserInfo(BaseModel):
    email: EmailStr
    password: str = Field(..., min_length=4)
    first_name: str
    last_name: str
    phone_number:Optional[str]

class Userlogin(BaseModel):
    email: EmailStr
    password: str = Field(..., min_length=4)
















