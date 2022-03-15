from os import environ 
from database import db 
from pyrogram.types import Message, InlineKeyboardButton, InlineKeyboardMarkup

class temp(object):
   GROUPS = []
   API_ID = int(environ.get("API_ID"))
   API_HASH = environ.get("API_HASH")
   BOT_TOKEN = environ.get("BOT_TOKEN")
   SESSION = environ.get("SESSION")
   LOG_CHANNEL = int(environ.get("LOG_CHANNEL"))

async def is_chat(_, bot, message: Message):
    if not message.from_user.is_bot:
       if message.text.startswith("/"):
         return False
    return True
    
async def buttons(chat):
   settings = await db.get_settings(chat)
   if settings["mode"] =="whitelist":
      text = "blacklist"
   elif settings["mode"] =="blacklist":
      text = "delete"
   elif settings["mode"] =="delete":
      text = "whitelist"
   if settings is not None:
      button=[[
         InlineKeyboardButton(f'Auto delete 🗑️', callback_data =f"done#auto_delete#{settings['auto_delete']}"), InlineKeyboardButton('OFF ❌' if settings['auto_delete'] else 'ON ✅', callback_data=f"done_#auto_delete#{settings['auto_delete']}")
        # ],[ 
       #  InlineKeyboardButton(f'Timer 🕐', callback_data =f"done#time#{settings['time']}"), InlineKeyboardButton(f'{settings['time']}', callback_data=f"done_#time#{settings['time']}")
         ],[
         InlineKeyboardButton(f'Delete Mode ⚙️', callback_data =f"done#mode#{text}"), InlineKeyboardButton(f'{text}', callback_data=f"done_#mode#{text}")
         ],[
         InlineKeyboardButton(f'Ignore admins 👱', callback_data =f"done#admins#{settings['admins']}"), InlineKeyboardButton('OFF ❌' if not settings['admins'] else 'ON ✅', callback_data=f"done_#admins#{settings['admins']}")
         ],[
         InlineKeyboardButton(f'Next ▶️', callback_data =f"others")
      ]]
   return InlineKeyboardMarkup(button)
  
def list_to_str(k):
    if not k:
        return 0
    elif len(k) == 1:
        return str(k[0])
    else:
        return ' '.join(f'{elem}' for elem in k)
