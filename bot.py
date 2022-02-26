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
    #if await db.add_chat(message.chat.id, message.chat.title):
      # total=await Bot.get_chat_members_count(message.chat.id)
      # await Bot.send_message(LOG_CHANNEL, f"#new group:\nTitle - {message.chat.title}\nId - {message.chat.id}\nTotal members - {total} added by - None")

#@User.on_message(filters.group & filters.text)
async def delete(user, message):
    data = await db.get_settings(message.chat.id)
    if not data["auto_delete"]: return
    try:
       time= "30"#data["time"]
       await asyncio.sleep(int(time))
       await Bot.delete_messages(message.chat.id, message.message_id)
    except Exception as e:
       print(e)
  
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
      done = await save_group_settings(group, type, False)
   else:
      done = await save_group_settings(group, type, True)
   await msg.message.edit_reply_markup(reply_markup=await buttons(group))
  
async def buttons(chat):
   settings = await db.get_settings(chat)
   if settings is not None:
      button=[[
         InlineKeyboardButton(f'Auto delete 🗑️', callback_data =f"done#auto_delete#{settings['auto_delete']}"), InlineKeyboardButton('OFF ❌' if settings['auto_delete'] else 'ON ✅', callback_data=f"done_#auto_delete#{settings['auto_delete']}")
         ],[ 
         InlineKeyboardButton(f'Timer 🕐', callback_data =f"done#time#{settings['time']}"), InlineKeyboardButton('OFF ❌' if settings['time'] else 'ON ✅', callback_data=f"done_#time#{settings['time']}")
         ],[
         InlineKeyboardButton(f'delete Mode ⚙️', callback_data =f"done#mode#{settings['mode']}"), InlineKeyboardButton('OFF ❌' if settings['mode'] else 'ON ✅', callback_data=f"done_#mode#{settings['mode']}")
         ],[
         InlineKeyboardButton(f'Ignore admins 👱', callback_data =f"done#admins#{settings['admins']}"), InlineKeyboardButton('OFF ❌' if not settings['admins'] else 'ON ✅', callback_data=f"done_#admins#{settings['admins']}")
      ]]
   return InlineKeyboardMarkup(button)
      
User.start()
print("User Started!")
Bot.start()
print("Bot Started!")

idle()

User.stop()
print("User Stopped!")
Bot.stop()
print("Bot Stopped!")
