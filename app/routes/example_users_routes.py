# app/routes/example_users_routes.py

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.models.user import User
from app.utils.response import json_response

router = APIRouter(tags=["Users"])


@router.get("/users/examples")
def get_example_users(db: Session = Depends(get_db)):
    """
    Returns a list of predefined example users.

    - No authentication required.
    - Passwords are manually assigned for demonstration purposes.
    - Includes additional fields: user_id, user_email, user_language, user_role, and is_active status.

    Args:
        db (Session): SQLAlchemy database session.

    Returns:
        JSONResponse: Response containing a list of example users with credentials and metadata.
    """
    # Predefined emails for example users
    example_emails = [
        "user@example.net",
        "admin@example.net",
        "superadmin@example.net",
        "inactive@example.net"
    ]

    # Manually assigned example passwords
    passwords = {
        "user@example.net": "userPassword",
        "admin@example.net": "adminPassword",
        "superadmin@example.net": "superadminPassword",
        "inactive@example.net": "inactivePassword"
    }

    # Retrieve users from the database
    users = db.query(User).filter(User.email.in_(example_emails)).all()

    # Format response payload
    data = []
    for user in users:
        data.append({
            "user_id": user.id,
            "user_name": user.name,
            "user_email": user.email,
            "user_password": passwords.get(user.email),
            "user_language": user.language.code if user.language else None,
            "user_role": user.role.name if user.role else None,
            "user_active": user.is_active
        })

    return json_response(
        success=True,
        message="Example users retrieved successfully",
        data=data
    )
