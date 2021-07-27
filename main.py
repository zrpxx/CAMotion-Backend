from typing import Optional
from fastapi.middleware.cors import CORSMiddleware
from fastapi import FastAPI
from pydantic import BaseModel
import database
from typing import List

from fastapi import FastAPI, WebSocket, WebSocketDisconnect
from fastapi.responses import HTMLResponse


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
    delete_img: str
    img_url: str


class Camera(BaseModel):
    uid: int = None
    name: str = None


class theCamera(BaseModel):
    id: int = None
    cid: int = None


class Report(BaseModel):
    user_id: int
    info: str


class Setting(BaseModel):
    user_id: int
    notify: int
    email: str

app = FastAPI()


class UserConnectionManager:
    def __init__(self):
        # 存放激活的ws连接对象
        self.active_connections = {}

    async def connect(self, ws: WebSocket, user: str):
        await ws.accept()
        self.active_connections[user] = ws
        print("New ws connection, ", self.active_connections)

    def disconnect(self, ws: WebSocket):
        for key, value in self.active_connections.items():
            if value == ws:
                del self.active_connections[key]
                print("Closed ws connection, ", self.active_connections)
                return

    async def send_personal_message(message: str, user: str):
        for _user, connection in self.active_connections.items():
            if _user == user:
                await connection.send_text(message)
                return

    async def broadcast(self, message: str):
        for user, connection in self.active_connections:
            await connection.send_text(message)


user_manager = UserConnectionManager()


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
    result = database.create_log(log.camera_id, log.info, log.delete_img, log.img_url)
    return result


@app.post("/create_camera/")
async def create_camera(cams: Camera):
    result = database.create_cam(cams.uid, cams.name)
    return result


@app.post("/delete_camera")
async def delete_camera(delete: theCamera):
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


@app.get("/get_undo_repo/")
async def get_undo_repo():
    result = database.get_undo_repo()
    return result


@app.get("/get_report")
async def get_report(user_id: int):
    result = database.get_report(user_id=user_id)
    return result


@app.post("/delete_all_cam")
async def delete_all_cam(delete_uid: int):
    result = database.delete_all_cam(uid=delete_uid)
    return result


@app.post("/get_url")
async def get_url(info: theCamera):
    result = database.get_url(info.id, info.cid)
    return result


@app.get("/get_dashboard_info")
async def get_dashboard_info():
    result = database.get_dashboard_info()
    return result


@app.post("/set_user_setting")
async def set_user_setting(setting: Setting):
    result = database.set_user_setting(setting.user_id,setting.notify,setting.email)
    return result


@app.websocket("/ws/{user}")
async def websocket_endpoint(websocket: WebSocket, user: str):

    await user_manager.connect(websocket)

    try:
        while True:
            data = await websocket.receive_text()
            await manager.send_personal_message(f"你说了: {data}", websocket)
            await manager.broadcast(f"用户:{user} 说: {data}")

    except WebSocketDisconnect:
        user_manager.disconnect(websocket)
        await manager.broadcast(f"用户-{user}-离开")


if __name__ == "__main__":
    import uvicorn
    # 官方推荐是用命令后启动 uvicorn main:app --host=127.0.0.1 --port=8010 --reload
    uvicorn.run(app='main:app', host="127.0.0.1", port=8010, reload=True, debug=True)



