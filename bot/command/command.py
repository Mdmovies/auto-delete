import asyncio 
import logging
from os import environ 
from database import db
from pyrogram import filters
from bot.main import User, Bot 
from .deleteall import delete_all
from pyrogram.errors import UserAlreadyParticipant, UserNotParticipant, ChatAdminInviteRequired
from pyrogram.errors.exceptions.forbidden_403 import ChatAdminRequired, MessageDeleteForbidden
from pyrogram.errors.exceptions.bad_request_400 import PeerIdInvalid, UserNotParticipant as UserNotMember
from pyrogram.types import InlineKeyboardButton, InlineKeyboardMarkup, Message
from configs import temp, is_chat, buttons, next_buttons, list_to_str, buttons as back_buttons, get_settings, save_settings

logging.basicConfig(level=logging.DEBUG,
                    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)
logging.getLogger("pyrogram").setLevel(logging.WARNING)

filters.chats=filters.create(is_chat)
TIME = {}
GROUPS = temp.GROUPS
USER_ID = temp.U_NAME

async def user_chat(bot: Bot, i, msg: Message):
    if msg.chat.type == "private":
        return False 
    if not msg.chat.id in GROUPS:
        return False
    await userbot_status(msg)
    try:
      user = await Bot.get_chat_member(msg.chat.id, USER_ID)
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
      user = await Bot.get_chat_member(msg.chat.id, USER_ID)
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
    data = await get_settings(chat)
    if not data["admins"]:
       st = await Bot.get_chat_member(chat, message.from_user.id)
       if st.status in ["administrator", "creator"]:
          return False
    try:
       time= data["time"]
       await asyncio.sleep(int(time))
       await Bot.delete_messages(chat, message.message_id)
    except MessageDeleteForbidden:
       return await Bot.send_message(chat, "please give me **Delete messages** permission to delete messages", parse_mode="md", reply_to_message_id=message.message_id)
    except Exception as e:
       logger.warning(e)
        
@Bot.on_message(filters.command("refresh"))
async def refresh_db(bot, message):
   user_id = message.from_user.id if message.from_user else 0
   if message.chat.type == "private":
      chat = await db.get_user_connection(str(user_id))
      if not chat:
         return await message.reply_text("I'm not connected to any groups!", quote=True)
   else:
      chat = message.chat.id
      st = await bot.get_chat_member(chat, user_id)
      if not (st.status in ["creator", "administrator"] or str(user_id) in [temp.user_id]):
         k=await message.reply_text("you are not group owner or admin")
         await asyncio.sleep(7)
         return await k.delete(True)
   default = await get_settings("01")
   await message.reply_text("✅ refreshed")
   temp.SETTINGS[chat] = default
   return await db.update_settings(int(chat), default)  
  
@Bot.on_message(filters.command("settings"))
async def withcmd(bot, message):
   user_id = message.from_user.id if message.from_user else 0  
   if message.chat.type == "private":
      chat = await db.get_user_connection(str(user_id))
      if not chat:
         return await message.reply_text("I'm not connected to any groups!", quote=True)
      ttl = await bot.get_chat(chat)
      title = ttl.title
   else:
      chat = message.chat.id
      title = message.chat.title
      st = await bot.get_chat_member(chat, user_id)
      if not (st.status in ["creator", "administrator"] or str(user_id) in [temp.user_id]):
         k=await message.reply_text("you are not group owner or admin")
         await asyncio.sleep(7)
         return await k.delete(True)
   await message.reply_text(f"<b><u>⚙️ SETTINGS</b></u>\n\n<b>Configure your group <code>{title}</code> deletion setting using below buttons</b>", reply_markup=await buttons(chat))
  
@Bot.on_callback_query(filters.regex(r"^done"))
async def settings_query(bot, msg):
   int, type, value, group, k = msg.data.split('#')
   user_id = msg.from_user.id if msg.from_user else 0    
   if msg.message.chat.type != "private":
      st = await bot.get_chat_member(group, user_id)
      if not (st.status == "creator" or st.status == "administrator" or str(user_id) in [temp.user_id]):
        return await msg.answer("you are not group owner or admin")
   if value=="True":
      await save_settings(group, type, False)
   elif type=="time":
      return await msg.answer("To change deletion time use /time <time in seconds>\neg:- /time 100", show_alert=True)
   elif value=="False":
      await save_settings(group, type, True)
   else:
      await save_settings(group, type, value)
   if k=="1":
     return await msg.message.edit_reply_markup(reply_markup=await back_buttons(group))
   return await msg.message.edit_reply_markup(reply_markup=await next_buttons(group))
    
@Bot.on_callback_query(filters.regex(r"^others"))
async def settings_query2(bot, msg):
   int, type, group = msg.data.split('#')
   user_id = msg.from_user.id if msg.from_user else 0  
   if msg.message.chat.type != "private":
      title = msg.message.chat.title
      st = await bot.get_chat_member(group, user_id)
      if not (st.status == "creator" or st.status == "administrator" or str(msg.from_user.id) in [temp.user_id]):
         return await msg.answer("you are not group owner or admin")
   else:
      ttl = await bot.get_chat(group)
      title = ttl.title
   if type=="1":
       return await msg.message.edit_text(text="Configure type of messages which will bot delete and not delete. using below buttons\n\n🗑️ = delete\n✖️ = do not delete",reply_markup=await next_buttons(group))
   elif type=="2":
       return await msg.message.edit_text(text= f"<b><u>⚙️ SETTINGS</b></u>\n\n<b>Configure your group <code>{title}</code> deletion setting using below buttons</b>", reply_markup= await back_buttons(group))
   elif type=="3":
       buttons = [[InlineKeyboardButton('✅ Confirm', callback_data=f"others#5#{group}")],[InlineKeyboardButton('❌ Cancel', callback_data=f"others#4#{group}")]]
       return await msg.message.edit_text(text="**🗑️ Delete all messages**\n\n**press confirm** to Delete all messages in group or **press cancel** to cancel process", reply_markup=InlineKeyboardMarkup(buttons))
   elif type=="4":
       return await msg.message.delete()
   if msg.message.chat.type == "private":
      return await msg.answer("you can only use this button in group", show_alert=True)
   st = await bot.get_chat_member(group, "me")
   if not (st.status=="administrator"):
      return await msg.answer("i not admin in group ! make me admin with full rights", show_alert=True)
   await msg.answer("processing...", show_alert=True)
   await delete_all(bot, msg.message)
   return
    
@Bot.on_message(filters.left_chat_member)
async def bot_kicked(c: Bot, m: Message):
    chat_id = m.chat.id
    left_member = m.left_chat_member
    if left_member.id == temp.bot_id:
        await db.remove_served_chat(chat_id)
        await c.send_message(temp.LOG_CHANNEL, f"#removed_serve_chat :\n**CHAT** - {m.chat.title} [<code>{m.chat.id}</code>]")
        try:
          await User.leave_chat(chat_id)
        except (UserNotParticipant, PeerIdInvalid):
          pass
        except Exception as e:
          await c.send_message(temp.LOG_CHANNEL, f"**ERROR WHEN USER LEAVE FROM CHAT **({chat_id})\n\n<code>{e}</code>")
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
        await c.send_message(temp.LOG_CHANNEL, f"#new_serve_chat :\n**CHAT** - {m.chat.title} [<code>{m.chat.id}</code>]")
    if temp.bot_id in [u.id for u in m.new_chat_members]:
       chats = await db.get_served_chats()
       temp.GROUPS = chats 
       await userbot_status(m)
    if await db.add_chat(m.chat.id, m.chat.title):
        total=await c.get_chat_members_count(m.chat.id)
        await c.send_message(temp.LOG_CHANNEL, "#New_Group :\n**Title** - {} [<code>{}</code>]\n**Total members** - {}\n**Added by** - {}".format(m.chat.title, m.chat.id, total, "Unknown"))
        await userbot_status(m) 
    return

async def userbot_status(m):
  c = Bot 
  user = User
  chat_id = m.chat.id
  try:
    b = await c.get_chat_member(chat_id, USER_ID) or await m.message.chat.get_member(USER_ID)
    if (b.status=="banned"):
      try:
         await c.unban_chat_member(chat_id=chat_id, user_id=temp.user_id)
      except ChatAdminRequired:
         await m.reply("My User bot is banned 🚫 in this Group.\ngive me admin permission **'Ban Users'** to unban")
      except BaseException:
         pass 
      invitelink = (await c.create_chat_invite_link(chat_id)).invite_link
      await user.join_chat(invitelink)
  except UserNotParticipant:
        try:
            invitelink = (await c.create_chat_invite_link(chat_id)).invite_link
            await user.join_chat(invitelink)
        except PeerIdInvalid as e:
            return False
        except (ChatAdminInviteRequired, ChatAdminRequired):
            time = TIME.get(chat_id)
            if not time:
              TIME[chat_id] = time = 0
            if time==0:
               await m.reply_text(f"Please Make Me Admin in Group With **'invite user via link'** and **'Delete messages'** permissions.\notherwise i cannot delete messages")
               TIME[chat_id] = 30
               await asyncio.sleep(30)
               TIME[chat_id] = 0
        except BaseException as e:
            await m.reply_text(
               f"❌ **userbot failed to join**\n\n**reason**: `{e}`")
  except (BaseException, PeerIdInvalid):
    pass
  return 
