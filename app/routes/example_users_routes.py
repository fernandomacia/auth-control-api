from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.models.user import User
from app.utils.response import json_response

router = APIRouter(tags=["Users"])

@router.get("/users/examples")
def get_example_users(db: Session = Depends(get_db)):
    """
    Returns a static list of example users fetched from the database.
    Passwords are assigned manually for testing purposes.
    No authentication required.
    """
    # Emails of example users
    example_emails = [
        "user@example.net",
        "admin@example.net",
        "superadmin@example.net",
        "inactive@example.net"
    ]

    # Plain passwords assigned manually
    passwords = {
        "user@example.net": "userPassword",
        "admin@example.net": "adminPassword",
        "superadmin@example.net": "superadminPassword",
        "inactive@example.net": "inactivePassword"
    }

    # Query users from database
    users = (
        db.query(User)
        .filter(User.email.in_(example_emails))
        .all()
    )

    # Build response data
    data = []
    for user in users:
        data.append({
            "user_name": user.name,
            "user_email": user.email,
            "user_password": passwords.get(user.email),
            "user_language": user.language.code if user.language else None,
            "user_role": user.role.name if user.role else None
        })

    return json_response(
        success=True,
        message="Example users retrieved successfully",
        data=data
    )
