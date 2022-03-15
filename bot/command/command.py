import asyncio
from os import environ 
from database import db 
from .deleteall import delete_all
from bot.main import User, Bot as BOT, User_bot, Bots
from pyrogram import Client as Bot, filters, idle 
from pyrogram.errors import UserAlreadyParticipant, UserNotParticipant
from pyrogram.types import InlineKeyboardButton, InlineKeyboardMarkup, Message
from configs import temp, is_chat, buttons, next_buttons, list_to_str
import logging
logging.basicConfig(level=logging.DEBUG,
                    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)
logging.getLogger("pyrogram").setLevel(logging.WARNING)

filters.chats=filters.create(is_chat)
START_MSG = "<b>Hai {},\nI'm a simple bot to delete group messages after a specific time</b>"
GROUPS = temp.GROUPS
USER_ID = 1411070838

async def user_chat(bot: Bot, i, msg: Message):
    if msg.chat.type == "private":
        return False
    await userbot_status(msg)
    try:
      user = await msg.chat.get_member(USER_ID)
    except UserNotParticipant:
      return False
    return True
filters.check=filters.create(user_chat)

async def bot_chat(bot: Bot, i, msg: Message):
    if msg.chat.type == "private":
        return False
    await userbot_status(msg)
    try:
      user = await msg.chat.get_member(USER_ID)
    except UserNotParticipant:
      return True
    return False
filters.checks=filters.create(bot_chat)

@Bot.on_message(filters.command('starts'))
async def starts(bot, message):
   await message.reply_text(f"processing {temp.GROUPS}")
   return
                           
@Bot.on_message(filters.command('start') & filters.private)
async def start(bot, cmd):
    await cmd.reply(START_MSG.format(cmd.from_user.mention))
    if await db.add_user(cmd.from_user.id, cmd.from_user.first_name):
        await bot.send_message(temp.LOG_CHANNEL, f"#NEWUSER: \nName - [{cmd.from_user.first_name}](tg://user?id={cmd.from_user.id})\nID - {cmd.from_user.id}")
        
@User_bot.on_message(filters.check & filters.chat(GROUPS) & filters.chats)#& ~filters.service_filter)#filters.text & filters.group & filters.incoming & filters.chats)
async def user_client(bot, message):
      # await message.reply_text("user")
       await delete(bot, message)
       return 
    
@Bot.on_message(filters.checks & filters.chat(GROUPS) & filters.chats)# & ~filters.service_filter)
async def bot_client(bot, message):
       await message.reply_text(f"bot")
       await delete(bot, message)
       return 
    
async def delete(bot, message):
    try:
       time= "4"#data["time"]
       await asyncio.sleep(int(time))
       await BOT.delete_messages(message.chat.id, message.message_id)
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
   await message.reply_text("✅ refreshed")
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
   int, type, value, k = msg.data.split('#')
   group = msg.message.chat.id
   st = await bot.get_chat_member(group, msg.from_user.id)
   if not (st.status == "creator") or (st.status == "administrator"):
      return await msg.answer("your not group owner or admin")
      
   if value=="True":
      await save_settings(group, type, False)
   elif type=="time":
      return await msg.answer("To change time use /time\neg:- /time 100 in seconds")
   elif value=="False":
      await save_settings(group, type, True)
   else:
      await save_settings(group, type, value)
   if k=="1":
     return await msg.message.edit_reply_markup(reply_markup=await buttons(group))
   return await msg.message.edit_reply_markup(reply_markup=await next_buttons(group))
    
@Bot.on_callback_query(filters.regex(r"^others"))
async def settings_query2(bot, msg):
   int, type= msg.data.split('#')
   group = msg.message.chat.id
   st = await bot.get_chat_member(group, msg.from_user.id)
   if not (st.status == "creator") or (st.status == "administrator"):
      return await msg.answer("your not group owner or admin")
   if type=="1":
       return await msg.message.edit_text(text="choose type of messages\n\n🗑️ - delete\n❌ - do not delete",reply_markup=await next_buttons(group))
   elif type=="2":
       return await msg.message.edit_text(text= "<b>change your group setting using below buttons</b>",reply_markup=await buttons(group))
   st = await bot.get_chat_member(group, "me")
   if not (st.status=="administrator"):
      await msg.answer("i not admin in group ! make me admin with full rights", show_alert=True)
   await msg.answer("processing...", show_alert=True)
   await delete_all(bot, msg.message)
   return
   
async def save_settings(group, key, value):
  current = await db.get_settings(int(group))
  current[key] = value 
  temp.SETTINGS[group] = current
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
       await userbot_status(m)
    return await m.reply(f"welcome to {m.chat.title}")

async def userbot_status(c, m):
  chat_id = m.chat.id
  try:
    b = await m.chat.get_chat_member(USER_ID)
    if (b.status=="banned"):
      try:
         await m.reply_text("❌ The userbot is banned in this chat, unban the userbot first to be able to delete message!")
      except BaseException:
         pass
      invitelink = (await c.get_chat(chat_id)).invite_link
      if not invitelink:
          await c.export_chat_invite_link(chat_id)
          invitelink = (await c.get_chat(chat_id)).invite_link
          if invitelink.startswith("https://t.me/+"):
             invitelink = invitelink.replace(
                    "https://t.me/+", "https://t.me/joinchat/"
                )
          await user.join_chat(invitelink)
  except UserNotParticipant:
        try:
            invitelink = (await c.get_chat(chat_id)).invite_link
            if not invitelink:
                await c.export_chat_invite_link(chat_id)
                invitelink = (await c.get_chat(chat_id)).invite_link
            if invitelink.startswith("https://t.me/+"):
                invitelink = invitelink.replace(
                    "https://t.me/+", "https://t.me/joinchat/"
                )
            await User_bot.join_chat(invitelink)
        except UserAlreadyParticipant:
            pass
        except Exception as e:
            await m.reply_text(
                f"❌ **userbot failed to join**\n\n**reason**: `{e}`")
  return
