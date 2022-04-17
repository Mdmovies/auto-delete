from os import environ 
from database import db
from pyrogram import filters
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
    chat = message.sender_chat
    user_id = chat.id if chat else message.from_user.id 
    if not get['auto_delete']:
        return False
    if get["mode"]=="whitelist" and await db.in_whitelist(user_id, m.chat.id):
        return False 
    elif get["mode"]=="blacklist" and not (await db.in_blacklist(user_id, m.chat.id)):
        return False 
    if not chat:
       if get["mode"]=="bots" and m.from_user.is_bot:
          return False
       elif user_id == temp.bot_id:
          return False
       elif not message.from_user.is_bot and not text is None and text.startswith("/"):
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
         InlineKeyboardButton(f'Auto delete 🗑️', callback_data =f"done#auto_delete#{settings['auto_delete']}#{chat}#1"), InlineKeyboardButton('OFF ❌' if settings['auto_delete'] else 'ON ✅', callback_data=f"done_#auto_delete#{settings['auto_delete']}#{chat}#1")
         ],[ 
         InlineKeyboardButton(f'Time 🕐', callback_data =f"done#time#{settings['time']}#{chat}#1"), InlineKeyboardButton(f"{settings['time']} s", callback_data=f"done_#time#{settings['time']}#{chat}#1")
         ],[
         InlineKeyboardButton(f'Delete Mode ⚙️', callback_data =f"done#mode#{text}#{chat}#1"), InlineKeyboardButton(f'{text}', callback_data=f"done_#mode#{mode}#{chat}#1")
         ],[
         InlineKeyboardButton(f'Ignore admins 👱', callback_data =f"done#admins#{settings['admins']}#{chat}#1"), InlineKeyboardButton('OFF ❌' if not settings['admins'] else 'ON ✅', callback_data=f"done_#admins#{settings['admins']}#{chat}#1")
         ],[
         InlineKeyboardButton(f'🗑️ Delete all messages', callback_data =f"others#3#{chat}")
         ],[
         InlineKeyboardButton(f'Next ▶️', callback_data =f"others#1#{chat}")
      ]]
   return InlineKeyboardMarkup(button)
 
async def next_buttons(chat):
   settings = await db.get_settings(chat)
   if settings is not None:
      button=[[
         InlineKeyboardButton(f'📷 photo', callback_data =f"done#photo#{settings['photo']}#{chat}#2"),
         InlineKeyboardButton('✖️' if settings['photo'] else '🗑️', callback_data=f"done_#photo#{settings['photo']}#{chat}#2")
         ],[ 
         InlineKeyboardButton(f'🎞️ video', callback_data =f"done#video#{settings['video']}#{chat}#2"),
         InlineKeyboardButton('✖️' if settings['video'] else '🗑️', callback_data=f"done_#video#{settings['video']}#{chat}#2")
         ],[ 
         InlineKeyboardButton(f'💾 file', callback_data =f"done#files#{settings['files']}#{chat}#2"),
         InlineKeyboardButton('✖️' if settings['files'] else '🗑️', callback_data=f"done_#files#{settings['files']}#{chat}#2")
         ],[ 
         InlineKeyboardButton(f'🎧 audio', callback_data =f"done#audio#{settings['audio']}#{chat}#2"),
         InlineKeyboardButton('✖️' if settings['audio'] else '🗑️', callback_data=f"done_#audio#{settings['audio']}#{chat}#2")
         ],[ 
         InlineKeyboardButton(f'🎤 voice', callback_data =f"done#voice#{settings['voice']}#{chat}#2"),
         InlineKeyboardButton('✖️' if settings['voice'] else '🗑️', callback_data=f"done_#voice#{settings['voice']}#{chat}#2")
         ],[ 
         InlineKeyboardButton(f'🎥 gifs', callback_data =f"done#gifs#{settings['gifs']}#{chat}#2"),
         InlineKeyboardButton('✖️' if settings['gifs'] else '🗑️', callback_data=f"done_#gifs#{settings['gifs']}#{chat}#2")
         ],[ 
         InlineKeyboardButton(f'📊 polls', callback_data =f"done#polls#{settings['polls']}#{chat}#2"),
         InlineKeyboardButton('✖️' if settings['polls'] else '🗑️', callback_data=f"done_#polls#{settings['polls']}#{chat}#2")
         ],[
         InlineKeyboardButton(f'🃏 sticker', callback_data =f"done#sticker#{settings['sticker']}#{chat}#2"),
         InlineKeyboardButton('✖️' if settings['sticker'] else '🗑️', callback_data=f"done_#sticker#{settings['sticker']}#{chat}#2")
         ],[ 
         InlineKeyboardButton(f'🎭 animated sticker', callback_data =f"done#emoji#{settings['emoji']}#{chat}#2"),
         InlineKeyboardButton('✖️' if settings['emoji'] else '🗑️', callback_data=f"done_#emoji#{settings['emoji']}#{chat}#2")
         ],[
         InlineKeyboardButton(f'◀️ back', callback_data =f"others#2#{chat}")
       ]]
   return InlineKeyboardMarkup(button)

async def verify_users(_,__, m: Message):
   if m.chat.type != "private":
     st = await m.chat.get_member(m.from_user.id)
     if not (st.status == "creator" or st.status == "administrator"):
        return False 
   return True 

verify = filters.create(verify_users)

def list_to_str(k):
    if not k:
        return 0
    elif len(k) == 1:
        return str(k[0])
    else:
        return ' '.join(f'{elem}' for elem in k)
