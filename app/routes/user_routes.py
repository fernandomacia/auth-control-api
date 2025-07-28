# app/routes/user_routes.py

from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.models.user import User
from app.models.language import Language
from app.schemas.user_schema import UpdateUserRequest
from app.services.users import get_current_user
from app.utils.response import json_response

router = APIRouter(prefix="/users/me", tags=["User"])

@router.put("")
def update_user(
    payload: UpdateUserRequest,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """
    Update the language preference of the authenticated user.
    
    - Requires valid and active authentication.
    - Returns 400 if the provided language code does not exist.
    - Returns updated language code on success.
    """
    language = db.query(Language).filter_by(code=payload.language_code).first()
    if not language:
        return json_response(False, "Language not found", status.HTTP_400_BAD_REQUEST)

    current_user.language_id = language.id
    db.commit()
    db.refresh(current_user)

    return json_response(
        success=True,
        message="User updated successfully",
        data={"user_language": language.code}
    )
