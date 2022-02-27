import asyncio
from os import environ 
from database import db
from pyrogram import Client, filters, idle
from pyrogram.types import InlineKeyboardButton, InlineKeyboardMarkup, Message
from configs import API_ID, API_HASH, BOT_TOKEN, SESSION, LOG_CHANNEL, GROUPS, is_chat, buttons

filters.chats=filters.create(is_chat)
START_MSG = "<b>Hai {},\nI'm a simple bot to delete group messages after a specific time</b>"

User = Client(session_name=SESSION,
              api_id=API_ID,
              api_hash=API_HASH,
              workers=300
              )


Bot = Client(session_name="auto-delete",
             api_id=API_ID,
             api_hash=API_HASH,
             bot_token=BOT_TOKEN,
             workers=300
             )

@Bot.on_message(filters.command('starts'))
async def starts(bot, message):
   k = await db.get_served_chats()
   total = len(k)
   GROUPS.append(k)
   await Bot.send_message(LOG_CHANNEL, f"restart successful and updated {total} chats")
   return
                           
@Bot.on_message(filters.command('start') & filters.private)
async def start(bot, cmd):
    await cmd.reply(START_MSG.format(cmd.from_user.mention))
    if await db.add_user(cmd.from_user.id, cmd.from_user.first_name):
        await bot.send_message(LOG_CHANNEL, f"#NEWUSER: \nName - [{cmd.from_user.first_name}](tg://user?id={cmd.from_user.id})\nID - {cmd.from_user.id}")
    
#GROUPS = -1001531562598
@User.on_message(filters.chat(await db.get_served_chats()))
async def delete(user, message):
    data = await db.get_settings(message.chat.id)
    if not data["auto_delete"]: return
    try:
       time= "30"#data["time"]
       await asyncio.sleep(int(time))
       await Bot.delete_messages(message.chat.id, message.message_id)
    except Exception as e:
       print(e)
        
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
    bot_id = Bot.get_me()
    chat_id = m.chat.id
    left_member = m.left_chat_member
    if left_member.id == bot_id.id:
        await db.remove_served_chat(chat_id)
        await c.send_message(LOG_CHANNEL, f"#removed_serve_chat:\nTitle - {m.chat.title}\nId - {m.chat.id}")
        await m.reply_text("👋👋👋👋👋")
    return 
  
@Bot.on_message(filters.new_chat_members)
async def new_chat(c: Bot, m: Message):
    chat_id = m.chat.id
    if await db.is_served_chat(chat_id):
        pass
    else:
        await db.add_served_chat(chat_id)
    if await db.add_chat(m.chat.id, m.chat.title):
       total=await c.get_chat_members_count(m.chat.id)
       await c.send_message(LOG_CHANNEL, f"#new group:\nTitle - {m.chat.title}\nId - {m.chat.id}\nTotal members - {total} added by - None")
    return await m.relpy_text(f"welcome to {m.chat.title}")

User.start()
print("User Started!")
Bot.start()
print("Bot Started!")

idle()

User.stop()
print("User Stopped!")
Bot.stop()
print("Bot Stopped!")
