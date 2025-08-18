# app/routes/admin_user_routes.py

from fastapi import APIRouter, Depends, status
from pydantic import BaseModel, Field, ConfigDict
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.models.user import User
from app.models.language import Language
from app.services.users import get_current_admin_or_superadmin_user
from app.utils.response import json_response

router = APIRouter(prefix="/users", tags=["Admin Users"])


class AdminUserPartialUpdate(BaseModel):
    """
    Partial update payload for admin user management.

    - Only the provided fields will be updated.
    - Unknown/extra fields are rejected.
    """
    model_config = ConfigDict(extra="forbid")

    language: str | None = Field(
        default=None,
        description="Language code, e.g. EN | ES | FR (case-insensitive)."
    )
    role: str | None = Field(
        default=None,
        description="Role name, e.g. Admin | SuperAdmin | User (case-insensitive)."
    )
    is_active: bool | None = Field(
        default=None,
        description="Active status flag."
    )


@router.patch("/{user_id}")
def admin_partial_update_user(
    user_id: int,
    payload: AdminUserPartialUpdate,
    db: Session = Depends(get_db),
    current_user=Depends(get_current_admin_or_superadmin_user)
):
    """
    Partially updates a user (admin scope).

    Rules
    -----
    - Only applies provided fields among {language, role, is_active}.
    - Fails on empty payload.
    - Validates that language and role exist.
    - Requires admin or superadmin.

    Responses follow the standard envelope: success, message, data.
    """
    # Fetch target user
    user = db.query(User).filter_by(id=user_id).first()
    if not user:
        return json_response(False, "User not found", status.HTTP_404_NOT_FOUND)

    # Reject empty payloads
    changes = payload.model_dump(exclude_none=True)
    if not changes:
        return json_response(False, "Empty payload not allowed", status.HTTP_400_BAD_REQUEST)

    # Apply updates conditionally
    # Track what changed to craft a clear message if needed
    updated_fields: list[str] = []

    # 1) is_active
    if "is_active" in changes:
        if not isinstance(changes["is_active"], bool):
            return json_response(False, "Invalid is_active value", status.HTTP_400_BAD_REQUEST)
        user.is_active = bool(changes["is_active"])
        updated_fields.append("is_active")

    # 2) language
    if "language" in changes:
        lang_code = str(changes["language"]).strip()
        if not lang_code:
            return json_response(False, "Invalid language value", status.HTTP_400_BAD_REQUEST)

        # Case-insensitive match against Language table
        language = db.query(Language).filter(Language.code.ilike(lang_code)).first()
        if not language:
            return json_response(False, "Language not found", status.HTTP_404_NOT_FOUND)

        user.language = language
        updated_fields.append("language")

    # 3) role
    if "role" in changes:
        role_name = str(changes["role"]).strip()
        if not role_name:
            return json_response(False, "Invalid role value", status.HTTP_400_BAD_REQUEST)

        # Late import to avoid circulars if any
        from app.models.user_role import UserRole as RoleModel

        role = db.query(RoleModel).filter(RoleModel.name.ilike(role_name)).first()
        if not role:
            return json_response(False, "Role not found", status.HTTP_404_NOT_FOUND)

        user.role_id = role.id
        updated_fields.append("role")

    # Persist only if something changed (safety)
    if not updated_fields:
        return json_response(False, "No valid fields to update", status.HTTP_400_BAD_REQUEST)

    db.commit()
    db.refresh(user)

    # Build response data snapshot
    data = {
        "user_id": user.id,
        "user_role": getattr(user.role, "name", None),
        "user_language": getattr(user.language, "code", None),
        "is_active": getattr(user, "is_active", None),
        "updated_fields": updated_fields,
    }

    return json_response(
        success=True,
        message="User partially updated",
        data=data,
    )
