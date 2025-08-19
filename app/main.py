# app/main.py

import os
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.routes import auth_routes, health_routes, user_routes, admin_user_routes, example_users_routes

app = FastAPI()

# --- CORS setup ---
# Parse ALLOWED_ORIGINS as CSV; fallback to localhost dev if unset/empty.
_env_origins = os.getenv("ALLOWED_ORIGINS", "")
allowed_origins = [o.strip() for o in _env_origins.split(",") if o.strip()]
if not allowed_origins:
    allowed_origins = ["http://localhost:4200", "http://127.0.0.1:4200"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=allowed_origins,
    allow_credentials=True,
    allow_methods=["GET", "POST", "PUT", "PATCH", "DELETE", "OPTIONS"],
    allow_headers=["Authorization", "Content-Type", "Accept", "Origin", "X-Requested-With"],
    expose_headers=["Content-Disposition"],
    max_age=600,
)

@app.get("/")
def read_root():
    """Simple liveness endpoint."""
    return {"message": "Auth Control API is running"}

# Routers
app.include_router(auth_routes.router)
app.include_router(user_routes.router)
app.include_router(admin_user_routes.router)
app.include_router(example_users_routes.router)
app.include_router(health_routes.router)
