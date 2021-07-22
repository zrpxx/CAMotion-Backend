from typing import Optional
from fastapi.middleware.cors import CORSMiddleware
from fastapi import FastAPI
from pydantic import BaseModel
import database
import test


class User(BaseModel):
    username: str
    password: str


class Item(BaseModel):
    status: str = None
    user_id: int = None
    message: str = None


class NewPassword(BaseModel):
    username: str
    password: str
    new_password: str


class Log(BaseModel):
    camera_id: int
    info: str
    attachment: str


class Camera(BaseModel):
    uid: int = None
    name: str = None
    url: str = None


class DelCamera(BaseModel):
    id: int = None
    cid: int = None


class Report(BaseModel):
    user_id: int
    info: str


app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=['*'],
    allow_credentials=True,
    allow_methods=['*', 'OPTIONS'],
    allow_headers=['*'],
)


@app.post("/login/")
async def login(user: User):
    result = database.login(user.username, user.password)
    return result


@app.post("/register/")
async def register(user: User):
    result = database.register(user.username, user.password)
    return result


@app.post("/modify_password/")
async def modify_password(user: NewPassword):
    result = database.modify_password(user.username, user.password, user.new_password)
    return result


@app.get("/cameras/{user_id}")
async def get_user_cameras(user_id: int):
    result = database.get_user_cameras(user_id=user_id)
    return result


@app.get("/get_camera_log/{camera_id}")
async def get_camera_log(camera_id: int):
    result = database.get_camera_log(camera_id=camera_id)
    return result


@app.get("/get_user_log/{user_id}")
async def get_user_log(user_id: int):
    result = database.get_user_log(user_id=user_id)
    return result


@app.post("/modify_password/")
async def modify_password(user: NewPassword):
    result = database.modify_password(user.username, user.password, user.new_password)
    return result


@app.post("/create_log/")
async def create_log(log: Log):
    result = database.create_log(log.camera_id, log.info, log.attachment)
    return result


@app.post("/create_camera/")
async def create_camera(cams: Camera):
    result = database.create_cam(cams.uid, cams.name, cams.url)
    return result


@app.post("/delete_camera")
async def delete_camera(delete: DelCamera):
    result = database.delete_cam(delete.id, delete.cid)
    return result


@app.get("/user/{user_id}")
async def get_user_info(user_id: int):
    result = database.get_user_info(user_id)
    return result


@app.post("/buy_vip/")
async def buy_vip(user_id: int):
    result = database.buy_vip(user_id)
    return result


@app.post("/create_report/")
async def create_report(report: Report):
    result = database.create_report(report.user_id, report.info)
    return result


@app.post("/change_report_status/")
async def change_report_status(repo_id: int, status: bool):
    result = database.change_report_status(repo_id=repo_id, status=status)
    return result
