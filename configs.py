from os import environ 
from database import db 
from pyrogram.types import Message, InlineKeyboardButton, InlineKeyboardMarkup

GROUPS = []
API_ID = int(environ.get("API_ID"))
API_HASH = environ.get("API_HASH")
BOT_TOKEN = environ.get("BOT_TOKEN")
SESSION = environ.get("SESSION")
LOG_CHANNEL = int(environ.get("LOG_CHANNEL"))

async def is_chat(_, bot, message: Message):
    chat_id = message.chat.id
    return chat_id in GROUPS
    
async def buttons(chat):
   settings = await db.get_settings(chat)
   if settings is not None:
      button=[[
         InlineKeyboardButton(f'Auto delete 🗑️', callback_data =f"done#auto_delete#{settings['auto_delete']}"), InlineKeyboardButton('OFF ❌' if settings['auto_delete'] else 'ON ✅', callback_data=f"done_#auto_delete#{settings['auto_delete']}")
         ],[ 
         InlineKeyboardButton(f'Timer 🕐', callback_data =f"done#time#{settings['time']}"), InlineKeyboardButton('OFF ❌' if settings['time'] else 'ON ✅', callback_data=f"done_#time#{settings['time']}")
         ],[
         InlineKeyboardButton(f'Delete Mode ⚙️', callback_data =f"done#mode#{settings['mode']}"), InlineKeyboardButton('OFF ❌' if settings['mode'] else 'ON ✅', callback_data=f"done_#mode#{settings['mode']}")
         ],[
         InlineKeyboardButton(f'Ignore admins 👱', callback_data =f"done#admins#{settings['admins']}"), InlineKeyboardButton('OFF ❌' if not settings['admins'] else 'ON ✅', callback_data=f"done_#admins#{settings['admins']}")
      ]]
   return InlineKeyboardMarkup(button)
  
def list_to_str(k):
    if not k:
        return 0
    elif len(k) == 1:
        return str(k[0])
    else:
        return ' '.join(f'{elem}' for elem in k)
