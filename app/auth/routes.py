# app/auth/routes.py

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.auth.schemas import LoginRequest, LoginResponse
from app.core.database import get_db
from app.models.user import User
from app.utils.security import verify_password, create_access_token

router = APIRouter(tags=["Auth"])

@router.post("/login", response_model=LoginResponse)
def login(request: LoginRequest, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.email == request.email).first()

    if not user:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid credentials")

    if not verify_password(request.password, user.hashed_password):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid credentials")
    
    if not user.is_active:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Inactive user")

    access_token = create_access_token(data={"sub": str(user.id)})

    return LoginResponse(
        access_token=access_token,
        user_id=user.id,
        user_name=user.name,
        user_email=user.email,
        user_role=user.role.name if user.role else None,
        user_language=user.language.code if user.language else None,
    )
