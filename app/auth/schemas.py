# app/auth/schemas.py

from pydantic import BaseModel, EmailStr

class LoginRequest(BaseModel):
    email: EmailStr
    password: str

class LoginResponse(BaseModel):
    access_token: str
    user_name: str
    user_role: str
    user_language: str
