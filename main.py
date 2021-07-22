from typing import Optional

from fastapi import FastAPI
from pydantic import BaseModel
import database
import test


class User(BaseModel):
    username: str
    password: str
    modified_password: Optional[str]


class Item(BaseModel):
    status: str = None
    user_id: int = None
    message: str = None


app = FastAPI()


@app.post("/login/")
async def login(user: User):
    result = database.login(user.username, user.password)
    return result


@app.post("/register/")
async def register(user: User):
    result = database.register(user.username, user.password)
    return result


@app.post("/modify_password/")
async def modify_password(user: User):
    result = database.modify_password(user.username, user.password, user.modified_password)
    return result
