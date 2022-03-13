import asyncio
from os import environ 
from database import db 
from bot.main import Bot as User
from pyrogram import Client as Bot, filters, idle 
from pyrogram.errors import UserAlreadyParticipant, UserNotParticipant
from pyrogram.types import InlineKeyboardButton, InlineKeyboardMarkup, Message
from configs import temp, is_chat, buttons, list_to_str
import logging
logging.basicConfig(level=logging.DEBUG,
                    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)
logging.getLogger("pyrogram").setLevel(logging.WARNING)

filters.chats=filters.create(is_chat)
START_MSG = "<b>Hai {},\nI'm a simple bot to delete group messages after a specific time</b>"
GROUPS = temp.GROUPS

@Bot.on_message(filters.command('starts'))
async def starts(bot, message):
   await message.reply_text(f"processing {temp.GROUPS}")
   return
                           
@Bot.on_message(filters.command('start') & filters.private)
async def start(bot, cmd):
    await cmd.reply(START_MSG.format(cmd.from_user.mention))
    if await db.add_user(cmd.from_user.id, cmd.from_user.first_name):
        await bot.send_message(temp.LOG_CHANNEL, f"#NEWUSER: \nName - [{cmd.from_user.first_name}](tg://user?id={cmd.from_user.id})\nID - {cmd.from_user.id}")
    
#GROUPS = -1001531562598
try:
  @User.on_message(filters.chat(GROUPS))#& ~filters.service_filter)#filters.text & filters.group & filters.incoming & filters.chats)
  async def user_client(bot, message):
       await message.reply_text("user")
       await delete(bot, message)
       return
except UserNotParticipant as e:
  @Bot.on_message(filters.chat(GROUPS))# & ~filters.service_filter)
  async def bot_client(bot, message):
       await message.reply_text(f"bot {e}")
       await delete(bot, message)
       return 
    
async def delete(bot, message):
   # if not message.chat.id == GROUPS: return
    await message.reply_text("hi")
  #  data = await db.get_settings(message.chat.id)
#    if not data["auto_delete"]: return
    try:
       time= "7"#data["time"]
       await asyncio.sleep(int(time))
       await bot.delete_messages(message.chat.id, message.message_id)
    except Exception as e:
       logger.warning(e)
        
@Bot.on_message(filters.command("refresh") & filters.group)
async def refresh_db(bot, message):
   st = await bot.get_chat_member(message.chat.id, message.from_user.id)
   if not (st.status == "creator") or (st.status == "administrator"):
      k=await message.reply_text("your not group owner or admin")
      await asyncio.sleep(7)
      return await k.delete(True)
   default = await db.get_settings("01")
   return await db.update_settings(message.chat.id, default)  
  
@Bot.on_message(filters.command("settings") & filters.group)
async def withcmd(bot, message):
   chat = message.chat.id
   user = message.from_user.id
   st = await bot.get_chat_member(chat, user)
   if not (st.status == "creator") or (st.status == "administrator"):
      k=await message.reply_text("your not group owner or admin")
      await asyncio.sleep(7)
      return await k.delete(True)
   await message.reply_text("<b>change your group setting using below buttons</b>", reply_markup=await buttons(chat))
  
@Bot.on_callback_query(filters.regex(r"^done"))
async def settings_query(bot, msg):
   int, type, value = msg.data.split('#')
   group = msg.message.chat.id
   st = await bot.get_chat_member(group, msg.from_user.id)
   if not (st.status == "creator") or (st.status == "administrator"):
      return await msg.answer("your not group owner or admin")
      
   if value=="True":
      done = await save_settings(group, type, False)
   else:
      done = await save_settings(group, type, True)
   await msg.message.edit_reply_markup(reply_markup=await buttons(group))

async def save_settings(group, key, value):
  current = await db.get_settings(int(group))
  current[key] = value 
  await db.update_settings(group, current)
  return

@Bot.on_message(filters.left_chat_member)
async def bot_kicked(c: Bot, m: Message):
    chat_id = m.chat.id
    left_member = m.left_chat_member
    if left_member.id == c.ID:
        await db.remove_served_chat(chat_id)
        await c.send_message(temp.LOG_CHANNEL, f"#removed_serve_chat:\nTitle - {m.chat.title}\nId - {m.chat.id}")
        await asyncio.sleep(5)
        chats = await db.get_served_chats()
        temp.GROUPS = chats
    return 
  
@Bot.on_message(filters.new_chat_members)
async def new_chat(c: Bot, m):
    chat_id = m.chat.id
    if await db.is_served_chat(chat_id):
        pass
    else:
        await db.add_served_chat(chat_id)
        await c.send_message(temp.LOG_CHANNEL, f"#NEW_SERVE_CHAT:\nTitle - {m.chat.title}\nId - {m.chat.id}")
        chats = await db.get_served_chats()
        temp.GROUPS = chats
    if await db.add_chat(m.chat.id, m.chat.title):
       total=await c.get_chat_members_count(m.chat.id)
       await c.send_message(temp.LOG_CHANNEL, f"#new group:\nTitle - {m.chat.title}\nId - {m.chat.id}\nTotal members - {total} added by - None")
    return await m.reply(f"welcome to {m.chat.title}")



