# import json
#
# from fastapi import WebSocket, APIRouter
# from sqlalchemy import create_engine
# from sqlalchemy.orm import sessionmaker
# import qrcode
# from auth.database import User, DATABASE_URL
# from my_telethon import my_qr_login, client
#
#
# router = APIRouter()
#
#
# # Словарь для хранения состояния авторизации по WebSocket
# authorization_status = {"authorized": False, "user_data": {}}
#
#
# @router.websocket("/ws")
# async def websocket_endpoint(websocket: WebSocket):
#     await websocket.accept()
#     try:
#         print("Этот вебсокет!")
#         # Ожидание QR-кода и получение данных пользователя
#         qr_login = await my_qr_login(client)
#         print("Этот вубсокет!", qr_login)
#         # Генерируем QR-код и сохраняем его как изображение
#         qr = qrcode.main.QRCode(
#             version=1,
#             box_size=10,
#             border=5,
#         )
#         # Используем другой метод кодирования URL
#         qr_url = qr_login.url
#         qr.add_data(qr_url)
#         qr.make(fit=True)
#         img = qr.make_image(fill_color="black", back_color="white")
#         img_path = "./static/qr_code/qr_code.png"
#         img.save(img_path)
#
#         await websocket.send_text(json.dumps({"qr_code_url": f"../static/qr_code/qr_code.png"}))
#
#         # Ожидание завершения авторизации
#         user = await qr_login.wait()
#         authorization_status["authorized"] = True
#         authorization_status["user_data"] = {"id": user.id, "username": user.username}
#         await websocket.send_text(
#             json.dumps({"status": "success", "user": {"id": user.id, "username": user.username}}))
#         new_user = User(id=user.id, username=user.username, email='dima@mail.ru', password='1234')
#
#         engine = create_engine(DATABASE_URL)
#         SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
#
#         db = SessionLocal()
#         db.add(new_user)
#
#         db.commit()
#
#     except Exception as e:
#         error_message = str(e) if str(e) else "Unknown error"
#         await websocket.send_text(json.dumps({"status": "error", "error": error_message}))
