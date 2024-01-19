import asyncio
from starlette.responses import JSONResponse
from telethon import TelegramClient
from base64 import urlsafe_b64encode as base64url
from qrcode.main import QRCode

api_id = 28305916
api_hash = '28d283dc40c4866bd7cc7eb6219484b0'
client = TelegramClient('SessionName', api_id, api_hash)

qr = QRCode()


async def my_qr_login(client: TelegramClient):
    if not client.is_connected():
        await client.connect()
    qr_login = await client.qr_login()
    # display_url_as_qr(qr_login.url)
    # print(qr_login.url)
    print("Запустил код!", qr_login.url)
    return qr_login




async def main():
    # Получение информации о себе
    # me = await client.get_me()

    # "me" - это пользовательский объект. Вы можете красиво напечатать
    # любой объект Telegram с помощью метода "stringify":
    # print(me.stringify())

    # Когда вы печатаете что-либо, вы видите его представление.
    # Вы можете получить доступ ко всем атрибутам объектов Telegram с помощью
    # оператора точки. Например, чтобы получить имя пользователя:
    # username = me.username
    # print(username)
    # print(me.phone)

    # Вы можете распечатать все диалоги / беседы, частью которых вы являетесь:
    # async for dialog in client.iter_dialogs():
    #     print(dialog.name, 'has ID', dialog.id)

    # Вы можете отправлять сообщения самому себе...
    # await client.send_message('me', 'Hello, myself!')
    # ...to some chat ID
    await client.send_message(763907255, 'Hello, group!')
    # ...вашим контактам
    # await client.send_message('+79269067556', 'Hello, friend!')
    # ...или даже к любому имени пользователя
    # await client.send_message('username', 'Testing Telethon!')

    # Вы, конечно, можете использовать markdown в своих сообщениях:
    # message = await client.send_message(
    #     'me',
    #     'This message has **bold**, `code`, __italics__ and '
    #     'a [nice website](https://example.com)!',
    #     link_preview=False
    # )

    # Отправка сообщения возвращает объект отправленного сообщения, который вы можете использовать для
    # print(message.raw_text)

    # Вы можете отвечать на сообщения напрямую, если у вас есть объект сообщения,
    # await message.reply('Cool!')

    # Или отправлять файлы, песни, документы, альбомы...
    # await client.send_file('me', '/home/dima_protasevich/Изображения/Alexios Assassins Creed Odyssey (3440x1440).jpg')

    # Вы можете распечатать историю сообщений любого чата:
    # async for message in client.iter_messages('me'):
    #     print(message.id, message.text, message.date, message)
    #
    #     # Вы также можете загружать медиафайлы из сообщений!
    #     # Метод вернет путь, по которому был сохранен файл.
    #     if message.photo:
    #         path = await message.download_media()
    #         print('File saved to', path)  # printed after download is done


async def get_profile():
    async with client:
        me = await client.get_me()
        username = me.username
        phone = me.phone
        first_name = me.first_name
        user_id = me.id
        return {'id': user_id, 'username': username, 'phone': phone, 'first_name': first_name}


async def get_dialogs():
    async with client:
        list = []
        async for dialog in client.iter_dialogs():
            item = {'dialogs_name': dialog.name, 'hash_id': dialog.id}
            list.append(item)
        return list


async def get_message_chat(id_chat: int, count: int = 20):
    async with client:
        messages = []
        limit = 0
        async for message in client.iter_messages(id_chat):
            mes = {'message_id': message.id, 'text': message.text, 'date': message.date, 'peer_id': message.peer_id, 'from_id': message.from_id}
            messages.append(mes)
            if limit == count:
                break
            else:
                limit += 1
        return messages


async def send_message(hsah: int, message: str):
    async with client:
        return await client.send_message(hsah, message)



# with client:
#
#     client.loop.run_until_complete(my_qr_login(client))
#     client.loop.run_until_complete(main())
#     client.loop.run_until_complete(get_profile())
