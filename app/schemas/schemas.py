from datetime import datetime
from typing import Optional

from pydantic import BaseModel, model_validator, Field, EmailStr


# models for basic endpoints

class UserCreate(BaseModel):
    email:EmailStr = Field(...,example="test@example.com")
    password: str =  Field(...,example='qwerty123')
    password2: str =  Field(...,example='qwerty123')
    first_name:str =  Field(...,example='test')
    last_name:str =  Field(...,example='test_1')


class UserUpdate(BaseModel):
    first_name: Optional[str] =  None
    last_name: Optional[str] =  None

class UserResponse(BaseModel):
    id: int
    email:str
    first_name: str
    last_name: str
    is_active: bool
    created_at: datetime

class LoginRequest(BaseModel):
    email: str
    password: str

class TokenResponse(BaseModel):
    access_token: str
    token_type: str = Field(default='Bearer')

class RefreshRequest(BaseModel):
    refresh_token: str

class MessageResponse(BaseModel):
    message: str


# models for admin's endpoints (in development)

# class UserRoleUpdate(BaseModel):
#     role_name:str

# class PermissionCreate(BaseModel):
#     resource_name:str
#     can_read:bool
#     can_write:bool
#     can_delete:bool

