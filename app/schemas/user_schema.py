# app/schemas/user_schemas.py

from pydantic import BaseModel, Field


class UpdateUserRequest(BaseModel):
    """
    Schema for updating the authenticated user's language.

    Attributes:
        language_code (str): Language code to apply (e.g., 'en', 'es').
    """
    language_code: str = Field(..., description="Language code (e.g., 'en', 'es')")


class ToggleActiveRequest(BaseModel):
    """
    Schema for toggling the `is_active` status of a user.

    Attributes:
        is_active (bool): Desired active status.
    """
    is_active: bool = Field(..., description="Desired active status (true or false)")
