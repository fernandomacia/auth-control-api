# app/main.py

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from dotenv import load_dotenv
import os

from app.auth import routes as auth_routes
from app.routes import user_routes as user_routes

# Load environment variables from .env file
load_dotenv()

# Parse allowed CORS origins from environment variable
origins = os.getenv("ALLOWED_ORIGINS", "").split(",")

# Initialize FastAPI application
app = FastAPI()

# Apply CORS middleware
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
    Basic health check route.
    
    Returns a simple JSON message confirming the API is running.
    """
    return {"message": "Auth Control API is running"}

# Register authentication and user-related routes
app.include_router(auth_routes.router)
app.include_router(user_routes.router)
