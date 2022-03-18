import asyncio 
import logging
from os import environ 
from database import db 
from pyrogram import filters
from bot.main import User, Bot
from .deleteall import delete_all
from configs import temp, is_chat, buttons, next_buttons, list_to_str
from pyrogram.errors import UserAlreadyParticipant, UserNotParticipant 
from pyrogram.errors.exceptions.bad_request_400 import ChatAdminRequired
from pyrogram.types import InlineKeyboardButton, InlineKeyboardMarkup, Message

logging.basicConfig(level=logging.DEBUG,
                    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)
logging.getLogger("pyrogram").setLevel(logging.WARNING)

filters.chats=filters.create(is_chat)
TIME = {}
GROUPS = temp.GROUPS
USER_ID = temp.user_id

async def user_chat(bot: Bot, i, msg: Message):
    if msg.chat.type == "private":
        return False 
    if not msg.chat.id in GROUPS:
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
    if msg.chat.id in GROUPS:
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
   
@User.on_message(filters.check & filters.chat(GROUPS) & filters.chats)#& ~filters.service_filter)#filters.text & filters.group & filters.incoming & filters.chats)
async def user_client(bot, message):
    await delete(bot, message)
    return 
    
@Bot.on_message(filters.checks & filters.chat(GROUPS) & filters.chats)# & ~filters.service_filter)
async def bot_client(bot, message):
    await delete(bot, message)
    return 
    
async def delete(bot, message):
    chat = message.chat.id
    data = await db.get_settings(chat)
    try:
       time= data["time"]
       await asyncio.sleep(int(time))
       await Bot.delete_messages(chat, message.message_id)
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
    if left_member.id == temp.bot_id:
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

async def userbot_status(m):
  c = Bot 
  user = User
  chat_id = m.chat.id
  try:
    b = await c.get_chat_member(chat_id, USER_ID) or await m.message.chat.get_member(USER_ID)
    if (b.status=="banned"):
      try:
         await m.reply_text("❌ The userbot is banned in this chat, unban the userbot first to be able to delete message!")
         await c.unban_chat_member(chat_id=chat_id, user_id=temp.user_id)
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
            await user.join_chat(invitelink)
        except UserAlreadyParticipant:
            pass 
        except ChatAdminRequired:
            time = TIME.get(chat_id)
            if not time:
              TIME[chat_id] = 0
            if time==0:
               await m.reply_text(f"please make me admin chat with all permissions otherwise i cannot delete messages")
               TIME[chat_id] = 30
               await asyncio.sleep(30)
               TIME[chat_id] = 0
        except Exception as e:
            await m.reply_text(
                f"❌ **userbot failed to join**\n\n**reason**: `{e}`")
  except BaseException as e:
    await m.reply_text(f"Error - {e}")
  return 
