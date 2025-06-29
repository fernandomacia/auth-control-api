# app/main.py
from fastapi import FastAPI

app = FastAPI()


@app.get("/")
def read_root():
    return {"message": "Auth Control API is running"}
