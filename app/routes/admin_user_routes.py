# app/routes/admin_user_routes.py

from fastapi import APIRouter, Depends, status, Body
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.models.user import User
from app.models.language import Language
from app.schemas.user_schema import ToggleActiveRequest
from app.services.users import get_current_admin_or_superadmin_user
from app.utils.response import json_response

router = APIRouter(prefix="/users", tags=["Admin Users"])


@router.put("/{user_id}/active")
def update_user_active_status(
    user_id: int,
    payload: ToggleActiveRequest,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_admin_or_superadmin_user)
):
    """
    Updates the `is_active` status of a user.

    - Requires admin or superadmin privileges.
    - Returns 404 if the user does not exist.
    - Returns 400 if `is_active` is not a boolean value.

    Args:
        user_id (int): Target user's ID.
        payload (ToggleActiveRequest): Contains the new `is_active` value.
        db (Session): SQLAlchemy database session.
        current_user (User): Authenticated admin or superadmin.

    Returns:
        JSONResponse: API response with success flag, message, and updated status.
    """
    user = db.query(User).filter_by(id=user_id).first()
    if not user:
        return json_response(False, "User not found", status.HTTP_404_NOT_FOUND)

    if not isinstance(payload.is_active, bool):
        return json_response(False, "Invalid is_active value", status.HTTP_400_BAD_REQUEST)

    user.is_active = payload.is_active
    db.commit()
    db.refresh(user)

    return json_response(
        success=True,
        message="User active status updated",
        data={"user_id": user.id, "is_active": user.is_active}
    )


@router.put("/{user_id}/language")
def update_user_language(
    user_id: int,
    language_code: str = Body(..., embed=False),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_admin_or_superadmin_user)
):
    """
    Updates the language of a specific user.

    - Requires admin or superadmin privileges.
    - Returns 404 if the user does not exist.
    - Returns 404 if the provided language does not exist.

    Args:
        user_id (int): Target user's ID.
        language_code (str): Language code (e.g., 'en', 'es').
        db (Session): SQLAlchemy database session.
        current_user (User): Authenticated admin or superadmin.

    Returns:
        JSONResponse: Operation result with updated `user_language` value.
    """
    user = db.query(User).filter_by(id=user_id).first()
    if not user:
        return json_response(False, "User not found", status.HTTP_404_NOT_FOUND)

    language = db.query(Language).filter_by(code=language_code.strip()).first()
    if not language:
        return json_response(False, "Language not found", status.HTTP_404_NOT_FOUND)

    user.language = language
    db.commit()
    db.refresh(user)

    return json_response(
        success=True,
        message="User language updated",
        data={"user_id": user.id, "user_language": user.language.code}
    )

@router.put("/{user_id}/role")
def update_user_role(
    user_id: int,
    role: str = Body(..., embed=False),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_admin_or_superadmin_user)
):
    """
    Updates the `role_id` of a user.

    - Requires admin or superadmin privileges.
    - Returns 404 if the user or role is not found.

    Args:
        user_id (int): Target user's ID.
        payload (dict): Should contain `role` (str).

    Returns:
        JSON response with updated user.
    """
    from app.models.user_role import UserRole

    user = db.query(User).filter_by(id=user_id).first()
    if not user:
        return json_response(False, "User not found", status.HTTP_404_NOT_FOUND)

    if not isinstance(role, str):
        return json_response(False, "Invalid role format", status.HTTP_400_BAD_REQUEST)

    role = db.query(UserRole).filter_by(name=role).first()
    if not role:
        return json_response(False, "Role not found", status.HTTP_404_NOT_FOUND)

    user.role_id = role.id
    db.commit()
    db.refresh(user)

    return json_response(
        success=True,
        message="User role updated",
        data={"user_id": user.id, "user_role": user.role.name}
    )