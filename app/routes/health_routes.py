# app/routes/health_routes.py

from fastapi import APIRouter

router = APIRouter()

@router.get("/health")
def health():
    """Liveness endpoint without DB access."""
    return {"status": "ok", "service": "auth-control-api"}
