# app/main.py

import os
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from dotenv import load_dotenv

from app.routes import auth_routes, user_routes, admin_user_routes, example_users_routes

# Load environment variables from .env file
load_dotenv()

# Parse allowed CORS origins from environment variable
origins = os.getenv("ALLOWED_ORIGINS", "").split(",")

# Initialize FastAPI application
app = FastAPI()

# Apply CORS configuration
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/")
def read_root():
    """
    Health check endpoint.

    Returns:
        dict: Confirmation that the API is operational.
    """
    return {"message": "Auth Control API is running"}

@app.get("/health")
def health():
    """Lightweight liveness probe."""
    return {"status": "ok"}

# Register API routes
app.include_router(auth_routes.router)
app.include_router(user_routes.router)
app.include_router(admin_user_routes.router)
app.include_router(example_users_routes.router)
