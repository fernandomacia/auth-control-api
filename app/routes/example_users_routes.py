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
        "superadmin@example.net"
    ]

    # Plain passwords assigned manually
    passwords = {
        "user@example.net": "user",
        "admin@example.net": "admin",
        "superadmin@example.net": "superadmin"
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
            "name": user.email,
            "password": passwords.get(user.email),
            "language": user.language.code if user.language else None,
            "role": user.role.name if user.role else None
        })

    return json_response(
        success=True,
        message="Example users retrieved successfully",
        data=data
    )
