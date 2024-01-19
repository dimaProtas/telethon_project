import json
from typing import Union

import bcrypt
import qrcode
from urllib.parse import quote
from fastapi.middleware.cors import CORSMiddleware
from fastapi import FastAPI, WebSocket, Depends
from fastapi_users import fastapi_users, FastAPIUsers
from pydantic import BaseModel
from sqlalchemy import create_engine, insert
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import sessionmaker, declarative_base
from starlette.responses import JSONResponse
from fastapi.staticfiles import StaticFiles
from fastapi.responses import HTMLResponse

from auth.auth import auth_backend
from auth.database import User, create_db_and_tables, DATABASE_URL, get_async_session
from auth.manager import get_user_manager
from auth.schemas import UserRead, UserCreate
from my_telethon import get_profile, get_dialogs, get_message_chat, send_message, my_qr_login, client
from parser.wildberis_parser import parser

app = FastAPI()

engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()


app.mount("/static", StaticFiles(directory="static"), name="static")

# Добавляем CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Разрешаем запросы из всех источников (здесь вы можете уточнить свой домен)
    allow_credentials=True,
    allow_methods=["*"],  # Разрешаем все методы (GET, POST, PUT, DELETE и другие)
    allow_headers=["*"],  # Разрешаем все заголовки
)

fastapi_users = FastAPIUsers[User, int](
    get_user_manager,
    [auth_backend],
)

app.include_router(
    fastapi_users.get_register_router(UserRead, UserCreate),
    prefix="/auth",
    tags=["auth"],
)

app.include_router(
    fastapi_users.get_auth_router(auth_backend),
    prefix="/auth/jwt",
    tags=["auth"],
)

@app.on_event("startup")
async def startup_event():
    await create_db_and_tables()


@app.get("/")
def read_root():
    return {'Hello': 'World'}


@app.get("/items/{item_id}")
def read_item(item_id: int, q: Union[str, None] = None):
    return {"item_id": item_id, "q": q}


@app.get("/profile")
async def profile():
    profile_data = await get_profile()
    return profile_data


@app.get("/dialogs")
async def dialogs():
    return await get_dialogs()


@app.get("/get_messages/{id_chat}")
async def message(id_chat: int, count: int = 20):
    messages = await get_message_chat(id_chat=int(id_chat), count=count)
    return messages


class Item(BaseModel):
    hash: int
    message: str


@app.post("/message")
async def send_message_api(item: Item):
    await send_message(item.hash, item.message)
    # print(item.hash, item.message)
    return {"status": "ok"}


# @app.get("/qr_login", response_class=HTMLResponse)
# async def login():
#     return {"status": "success"}


# Словарь для хранения состояния авторизации по WebSocket
authorization_status = {"authorized": False, "user_data": {}}


@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket, session: AsyncSession = Depends(get_async_session)):
    await websocket.accept()
    try:
        print("Этот вебсокет!")
        # Ожидание QR-кода и получение данных пользователя
        qr_login = await my_qr_login(client)
        print("Этот вубсокет!", qr_login)
        # Генерируем QR-код и сохраняем его как изображение
        qr = qrcode.main.QRCode(
            version=1,
            box_size=10,
            border=5,
        )
        # Используем другой метод кодирования URL
        qr_url = qr_login.url
        qr.add_data(qr_url)
        qr.make(fit=True)
        img = qr.make_image(fill_color="black", back_color="white")
        img_path = "./static/qr_code/qr_code.png"
        img.save(img_path)

        await websocket.send_text(json.dumps({"qr_code_url": f"../static/qr_code/qr_code.png"}))

        # Ожидание завершения авторизации
        user = await qr_login.wait()
        authorization_status["authorized"] = True
        authorization_status["user_data"] = {"id": user.id, "username": user.username}

        hashed_password = bcrypt.hashpw('1234'.encode('utf-8'), bcrypt.gensalt())

        new_user = insert(User).values(
            username=user.username,
            email=f'{user.id}@email.com',
            hashed_password=hashed_password.decode('utf-8'),
            is_active=True,
            is_superuser=False,
            is_verified=False
        )

        await session.execute(new_user)
        await session.commit()

        user = User(username=user.username, email=f'{user.id}@email.com', hashed_password='1234')

        auth_strategy = auth_backend.get_strategy()
        await auth_backend.login(auth_strategy, user=user)

        await websocket.send_text(
            json.dumps({"status": "success", "user": {"id": user.id, "username": user.username}}))

    except Exception as e:
        error_message = str(e) if str(e) else "Unknown error"
        await websocket.send_text(json.dumps({"status": "error", "error": error_message}))


@app.get('/wildberis/{search}')
async def wildberis(search: str):
    result = parser(search)
    return {'succes': 'ok', 'result': result}