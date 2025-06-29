# app/main.py

from fastapi import FastAPI
from app.auth import routes as auth_routes

app = FastAPI()


@app.get("/")
def read_root():
    return {"message": "Auth Control API is running"}

app.include_router(auth_routes.router)
