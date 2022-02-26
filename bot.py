import asyncio
from os import environ 
from database import db
from pyrogram import Client, filters, idle
from configs import API_ID, API_HASH, BOT_TOKEN, SESSION,  DATABASE, LOG_CHANNEL

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


@Bot.on_message(filters.command('start') & filters.private)
async def start(bot, cmd):
    await cmd.reply(START_MSG.format(cmd.from_user.mention))
    if await db.add_user(cmd.from_user.id, cmd.from_user.first_name):
        await bot.send_message(LOG_CHANNEL, f"#NEWUSER: \nName - [{cmd.from_user.first_name}](tg://user?id={cmd.from_user.id})\nID - {cmd.from_user.id}")

@Bot.on_message(filters.group & filters.incoming & filters.text)
async def delete(user, message):
    if await db.add_chat(message.chat.id, message.chat.title):
       total=await user.get_chat_members_count(cmd.chat.id)
       await user.send_message(LOG_CHANNEL, f"#new group:\nTitle - {message.chat.title}\nId - {message.chat.id}\nTotal members - {total} added by - None")
    data = await db.get_settings(message.chat.id)
    if not data["auto_delete"]: return
    try:
       time= "30"#data["time"]
       await asyncio.sleep(int(time))
       await Bot.delete_messages(message.chat.id, message.message_id)
    except Exception as e:
       print(e)
       
User.start()
print("User Started!")
Bot.start()
print("Bot Started!")

idle()

User.stop()
print("User Stopped!")
Bot.stop()
print("Bot Stopped!")
