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
   ADMINS = [environ.get("ADMINS", "0")]
   PASSWORD = environ.get("PASSWORD", None)
   LOG_CHANNEL = int(environ.get("LOG_CHANNEL"))

async def is_chat(_, bot, message: Message):
    m = message
    text = message.text
    get = await get_settings(m.chat.id)
    chat = message.sender_chat
    user_id = chat.id if chat else message.from_user.id
    if not get['auto_delete']:
        return False
    if get["mode"]=="whitelist" and await db.in_whitelist(int(user_id), int(m.chat.id)):
        return False 
    elif get["mode"]=="blacklist" and not (await db.in_blacklist(int(user_id), int(m.chat.id))):
        return False 
    if not chat:
       if get["mode"]=="bots" and m.from_user.is_bot:
          return False
       elif user_id == temp.bot_id:
          return False
       elif not message.from_user.is_bot and not text is None and text.startswith("/"):
          return False 
    msg = [[get["photo"], m.photo], [get["video"], m.video], [get["files"], m.document], [get["audio"], m.audio], [get["sticker"], m.sticker], [get["polls"], m.poll], [get["emoji"], m.animation]]
    for msg_type in msg:
       if not msg_typs[0] and msg_type[1]:
          return False 
    return True
    
async def buttons(chat):
   settings = await get_settings(chat)
   modes = settings["mode"]
   for x in [["whitelist", "blacklist", "blacklisted users"], ["bots", "delete", "All messages"], ["delete", "whitelist", "Except whitelisted"], ["blacklist", "bots", "Except Bots 🤖"]]
      if modes == x[0]:
        mode, text = x[1], x[2]
        break
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
   settings = await get_settings(chat)
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

async def get_settings(group):
  settings = temp.SETTINGS.get(int(group))
  if not settings:
     settings = await db.get_settings(group)
     temp.SETTINGS[int(group)] = settings 
  return settings

async def save_settings(group, key, value):
  current = await get_settings(int(group))
  current[key] = value 
  temp.SETTINGS[int(group)] = current
  await db.update_settings(group, current)
  
async def verify_users(_,__, m: Message):
   if m.chat.type != "private":
     user = m.from_user.id if m.from_user else None
     if not user:
        return
     st = await m.chat.get_member(user)
     if not st.status in ["creator", "administrator"]:
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
