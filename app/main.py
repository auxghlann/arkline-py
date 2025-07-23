from fastapi import FastAPI
from app.router.request import router as client_router

app = FastAPI()

app.include_router(client_router)

@app.get("/")
def read_root():
    return {"message": "Welcome to the Arkline AI API!"}