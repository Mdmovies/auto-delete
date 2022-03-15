from os import environ 
from database import db 
from pyrogram.types import Message, InlineKeyboardButton, InlineKeyboardMarkup

class temp(object):
   GROUPS = []
   SETTINGS = {}
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
      mode, text = "blacklist", "blacklisted users"
   elif settings["mode"] =="blacklist":
      mode, text = "delete", "All messages"
   elif settings["mode"] =="delete":
      mode, text = "whitelist", "except whitelisted"
   if settings is not None:
      button=[[
         InlineKeyboardButton(f'Auto delete 🗑️', callback_data =f"done#auto_delete#{settings['auto_delete']}#1"), InlineKeyboardButton('OFF ❌' if settings['auto_delete'] else 'ON ✅', callback_data=f"done_#auto_delete#{settings['auto_delete']}#1")
         ],[ 
         InlineKeyboardButton(f'Time 🕐', callback_data =f"done#time#{settings['time']}#1"), InlineKeyboardButton(f"{settings['time']} s", callback_data=f"done_#time#{settings['time']}#1")
         ],[
         InlineKeyboardButton(f'Delete Mode ⚙️', callback_data =f"done#mode#{text}#1"), InlineKeyboardButton(f'{text}', callback_data=f"done_#mode#{mode}#1")
         ],[
         InlineKeyboardButton(f'Ignore admins 👱', callback_data =f"done#admins#{settings['admins']}#1"), InlineKeyboardButton('OFF ❌' if not settings['admins'] else 'ON ✅', callback_data=f"done_#admins#{settings['admins']}#1")
         ],[
         InlineKeyboardButton(f'Next ▶️', callback_data =f"others#1")
      ]]
   return InlineKeyboardMarkup(button)
 
async def next_buttons(chat):
   settings = await db.get_settings(chat)
   if settings is not None:
      button=[[
         InlineKeyboardButton(f'📷 photo', callback_data =f"done#photos#{settings['photo']}#2"),
         InlineKeyboardButton('❌' if settings['photo'] else '🗑️', callback_data=f"done_#photo#{settings['photo']}#2")
         ],[ 
         InlineKeyboardButton(f'🎞️ video', callback_data =f"done#video#{settings['video']}#2"),
         InlineKeyboardButton('❌' if settings['video'] else '🗑️', callback_data=f"done_#video#{settings['video']}#2")
         ],[ 
         InlineKeyboardButton(f'💾 file', callback_data =f"done#files#{settings['files']}#2"),
         InlineKeyboardButton('❌' if settings['files'] else '🗑️', callback_data=f"done_#files#{settings['files']}#2")
         ],[ 
         InlineKeyboardButton(f'🎧 audio', callback_data =f"done#audio#{settings['audio']}#2"),
         InlineKeyboardButton('❌' if settings['audio'] else '🗑️', callback_data=f"done_#audio#{settings['audio']}#2")
         ],[ 
         InlineKeyboardButton(f'🎤 voice', callback_data =f"done#voice#{settings['voice']}#2"),
         InlineKeyboardButton('❌' if settings['voice'] else '🗑️', callback_data=f"done_#voice#{settings['voice']}#2")
         ],[ 
         InlineKeyboardButton(f'🎥 gifs', callback_data =f"done#gifs#{settings['gifs']}#2"),
         InlineKeyboardButton('❌' if settings['gifs'] else '🗑️', callback_data=f"done_#gifs#{settings['gifs']}#2")
         ],[ 
         InlineKeyboardButton(f'🃏 sticker', callback_data =f"done#sticker#{settings['sticker']}#2"),
         InlineKeyboardButton('❌' if settings['sticker'] else '🗑️', callback_data=f"done_#sticker#{settings['sticker']}#2")
         ],[ 
         InlineKeyboardButton(f'😎 emoji', callback_data =f"done#emoji#{settings['emoji']}#2"),
         InlineKeyboardButton('❌' if settings['emoji'] else '🗑️', callback_data=f"done_#emoji#{settings['emoji']}")
         ],[ 
         InlineKeyboardButton(f'📊 polls', callback_data =f"done#polls#{settings['polls']}#2"),
         InlineKeyboardButton('❌' if settings['polls'] else '🗑️', callback_data=f"done_#polls#{settings['polls']}#2")
         ],[
         InlineKeyboardButton(f'◀️ back', callback_data =f"others#2")
       ]]
   return InlineKeyboardMarkup(button)

def list_to_str(k):
    if not k:
        return 0
    elif len(k) == 1:
        return str(k[0])
    else:
        return ' '.join(f'{elem}' for elem in k)
