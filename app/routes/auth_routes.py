# app/routes/auth_routes.py

from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session
from app.schemas.auth_schema import LoginRequest
from app.core.database import get_db
from app.models.user import User
from app.utils.security import verify_password, create_access_token
from app.utils.response import json_response

router = APIRouter(tags=["Auth"])

@router.post("/login")
def login(request: LoginRequest, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.email == request.email).first()

    if not user:
        return json_response(False, "Invalid credentials", status.HTTP_401_UNAUTHORIZED)

    if not verify_password(request.password, user.hashed_password):
        return json_response(False, "Invalid credentials", status.HTTP_401_UNAUTHORIZED)
    
    if not user.is_active:
        return json_response(False, "Inactive user", status.HTTP_403_FORBIDDEN)

    access_token = create_access_token(data={"sub": str(user.id)})

    return json_response(
        success=True,
        message="Login successful",
        data={
            "access_token": access_token,
            "user_name": user.name,
            "user_role": user.role.name if user.role else None,
            "user_language": user.language.code if user.language else None,
        }
    )
