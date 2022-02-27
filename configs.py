from os import environ 
from database import db 
from pyrogram.types import Message 

GROUPS = []
API_ID = int(environ.get("API_ID"))
API_HASH = environ.get("API_HASH")
BOT_TOKEN = environ.get("BOT_TOKEN")
DATABASE = environ.get("DATABASE")
SESSION = environ.get("SESSION")
LOG_CHANNEL = int(environ.get("LOG_CHANNEL"))

async def is_chat(_, bot, message: Message):
    chat_id = message.chat.id
    xx = await db.get_settings(chat_id)
    if not await db.is_served_chat(chat_id):
      return False         
    if not xx["auto_delete"]:
      return False
    if not xx["bots"]:
      return False 
    if not int(chat_id) in GROUPS:
       GROUPS.append(int(chat_id))
    return True
filters.chats=filters.create(is_chat)
