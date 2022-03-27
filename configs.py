from os import environ 
from database import db
from pyrogram.types import Message, InlineKeyboardButton, InlineKeyboardMarkup

class temp(object):
   Bot = None 
   User = None 
   B_NAME = None 
   U_NAME = None
   bot_id = 0
   user_id = 0
   GROUPS = []
   SETTINGS = {}
   API_ID = int(environ.get("API_ID"))
   API_HASH = environ.get("API_HASH")
   BOT_TOKEN = environ.get("BOT_TOKEN")
   SESSION = environ.get("SESSION")
   PASSWORD = environ.get("PASSWORD", None)
   LOG_CHANNEL = int(environ.get("LOG_CHANNEL"))

async def is_chat(_, bot, message: Message):
    m = message
    text = message.text
    get = await db.get_settings(m.chat.id)
    if not get['auto_delete']:
        return False
    if get["mode"]=="whitelist" and await db.in_whitelist(m.from_user.id, m.chat.id):
        return False 
    elif get["mode"]=="blacklist" and not (await db.in_blacklist(m.from_user.id, m.chat.id)):
        return False 
    elif get["mode"]=="bots" and m.from_user.is_bot:
        return False
    if message.from_user.id == temp.bot_id:
       return False
    if not message.from_user.is_bot and not text is None and text.startswith("/"):
       return False 
    if not get["photo"] and m.photo:
       return False 
    elif not get["video"] and m.video:
       return False 
    elif not get["files"] and m.document:
       return False
    elif not get["audio"] and m.audio:
       return False
    elif not get["sticker"] and m.sticker:
       return False
    elif not get["polls"] and m.poll:
       return False 
    elif not get["emoji"] and m.animation:
       return False
    return True
    
async def buttons(chat):
   settings = await db.get_settings(chat)
   if settings["mode"] =="whitelist":
      mode, text = "blacklist", "blacklisted users"
   elif settings["mode"] =="bots":
      mode, text = "delete", "All messages"
   elif settings["mode"] =="delete":
      mode, text = "whitelist", "Except whitelisted"
   elif settings["mode"] =="blacklist":
      mode, text = "bots", "Except Bots 🤖"
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
         InlineKeyboardButton(f'🗑️ Delete all messages', callback_data =f"others#3")
         ],[
         InlineKeyboardButton(f'Next ▶️', callback_data =f"others#1")
      ]]
   return InlineKeyboardMarkup(button)
 
async def next_buttons(chat):
   settings = await db.get_settings(chat)
   if settings is not None:
      button=[[
         InlineKeyboardButton(f'📷 photo', callback_data =f"done#photos#{settings['photo']}#2"),
         InlineKeyboardButton('✖️' if settings['photo'] else '🗑️', callback_data=f"done_#photo#{settings['photo']}#2")
         ],[ 
         InlineKeyboardButton(f'🎞️ video', callback_data =f"done#video#{settings['video']}#2"),
         InlineKeyboardButton('✖️' if settings['video'] else '🗑️', callback_data=f"done_#video#{settings['video']}#2")
         ],[ 
         InlineKeyboardButton(f'💾 file', callback_data =f"done#files#{settings['files']}#2"),
         InlineKeyboardButton('✖️' if settings['files'] else '🗑️', callback_data=f"done_#files#{settings['files']}#2")
         ],[ 
         InlineKeyboardButton(f'🎧 audio', callback_data =f"done#audio#{settings['audio']}#2"),
         InlineKeyboardButton('✖️' if settings['audio'] else '🗑️', callback_data=f"done_#audio#{settings['audio']}#2")
         ],[ 
         InlineKeyboardButton(f'🎤 voice', callback_data =f"done#voice#{settings['voice']}#2"),
         InlineKeyboardButton('✖️' if settings['voice'] else '🗑️', callback_data=f"done_#voice#{settings['voice']}#2")
         ],[ 
         InlineKeyboardButton(f'🎥 gifs', callback_data =f"done#gifs#{settings['gifs']}#2"),
         InlineKeyboardButton('✖️' if settings['gifs'] else '🗑️', callback_data=f"done_#gifs#{settings['gifs']}#2")
         ],[ 
         InlineKeyboardButton(f'📊 polls', callback_data =f"done#polls#{settings['polls']}#2"),
         InlineKeyboardButton('✖️' if settings['polls'] else '🗑️', callback_data=f"done_#polls#{settings['polls']}#2")
         ],[
         InlineKeyboardButton(f'🃏 sticker', callback_data =f"done#sticker#{settings['sticker']}#2"),
         InlineKeyboardButton('✖️' if settings['sticker'] else '🗑️', callback_data=f"done_#sticker#{settings['sticker']}#2")
         ],[ 
         InlineKeyboardButton(f'🎭 animated sticker', callback_data =f"done#emoji#{settings['emoji']}#2"),
         InlineKeyboardButton('✖️' if settings['emoji'] else '🗑️', callback_data=f"done_#emoji#{settings['emoji']}#2")
         ],[
         InlineKeyboardButton(f'◀️ back', callback_data =f"others#2")
       ]]
   return InlineKeyboardMarkup(button)

async def verfiy_users(_,__, m: Message):
   st = await m.chat.get_chat_member(m.from_user.id)
   if chat.type == "private":
      return False
   if not (st.status == "creator") or (st.status == "administrator"):
      return False 
   return True 

def list_to_str(k):
    if not k:
        return 0
    elif len(k) == 1:
        return str(k[0])
    else:
        return ' '.join(f'{elem}' for elem in k)
