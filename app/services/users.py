# app/services/user.py

from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session
from jose import jwt, JWTError
from app.core.database import get_db
from app.models.user import User
import os

# OAuth2 scheme to extract the token from the Authorization header
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login")

# JWT configuration from environment variables
JWT_SECRET_KEY = os.getenv("JWT_SECRET_KEY")
JWT_ALGORITHM = os.getenv("JWT_ALGORITHM")


def get_current_user(
    token: str = Depends(oauth2_scheme),
    db: Session = Depends(get_db)
) -> User:
    print("Entrando en get_current_user")  # Depuración
    print("Token recibido:", token)  # Depuración
    try:
        payload = jwt.decode(token, JWT_SECRET_KEY, algorithms=[JWT_ALGORITHM])
        print("Payload decodificado:", payload)  # Depuración
        # Verifica si 'sub' está en el payload y es convertible a int
        if "sub" not in payload:
            print("El campo 'sub' no está en el payload")  # Depuración
            raise ValueError("No sub in payload")
        user_id = int(payload.get("sub"))
        print("user_id extraído:", user_id)  # Depuración
    except (JWTError, TypeError, ValueError) as e:
        print("Error decodificando el token o extrayendo user_id:", e)  # Depuración
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid authentication credentials",
        )

    user = db.query(User).filter_by(id=user_id).first()
    print("Usuario obtenido de la base de datos:", user)  # Depuración

    if user is None or not user.is_active:
        print("Usuario no existe o está inactivo")  # Depuración
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Inactive or invalid user",
        )

    print("user:", user.id, user.email)  # Muestra atributos específicos
    return user
    raise HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Inactive or invalid user",
    )

    print("user:", user.id, user.email)  # Muestra atributos específicos
    return user

