from fastapi import FastAPI, Depends
# from app.routers.requests import router as client_router
from typing import Annotated
from sqlalchemy.orm import Session
from app.db.session import get_db
from app.routers import auth, rtr_message
from app.routers.auth import get_current_user

app = FastAPI()

app.include_router(auth.router)
app.include_router(rtr_message.router)

db_dependency = Annotated[Session, Depends(get_db)]
user_dependency = Annotated[dict, Depends(get_current_user)]

@app.get("/")
def read_root():
    return {"message": "Welcome to the Arkline AI API!"}


# # test auth
# @app.get("/test-auth")
# def test_auth(current_user: user_dependency):
#     return {"message": f"Hello, {current_user['username']}! You are authenticated."}









