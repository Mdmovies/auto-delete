import asyncio 
from database import db
from pyrogram import filters 
from bot.main import Bot as Client 
from configs import verify, save_settings
from pyrogram.errors.exceptions.bad_request_400 import PeerIdInvalid 

@Client.on_message(filters.command('whitelist') & verify)
async def whitelist(client, message):
  data = await informations(client, message)
  if not data: 
     return
  chat_id, user_id, user_name = data
  add = await db.add_whitelist(user_id, int(chat_id))
  if not add:
    await message.reply_text(f"{user_name} already in whitelist")
  else:
    await message.reply_text(f"Successfully Added {user_name} to whitelist")
    
@Client.on_message(filters.command('rwhitelist') & verify)
async def rwhitelist(client, message):
  data = await informations(client, message)
  if not data: 
     return
  chat_id, user_id, user_name = data
  add = await db.remove_whitelist(user_id, int(chat_id))
  if not add:
    await message.reply_text(f"{user_name} not in whitelist")
  else:
    await message.reply_text(f"Successfully {user_name} removed from whitelist")

@Client.on_message(filters.command('gwhitelist') & verify)
async def get_all_whitelist(client, message):
  chat_type = message.chat.type
  if chat_type == "private":
     chat_id = await db.get_user_connection(str(message.from_user.id))
     if not chat_id:
        return await message.reply_text("I'm not connected to any groups!", quote=True)
  else:
     chat_id = message.chat.id
  msg = await message.reply_text("Processing.....")
  users = await db.get_chat_whitelists(int(chat_id))
  txt = "<b><u>whitelisted users are :-</b></u>\n\n"
  if users:
     async for user in users:
       try:
         k = await client.get_users(user['user_id'])
         txt+= f"<a href=tg://user?id={k.id}>{k.first_name}</a>\n"
       except IndexError:
         txt+= f"CHANNEL ({user['user_id']})"
  else:
     txt = "**No Whitelisted users in this Group**"
  return await msg.edit(txt)
  
@Client.on_message(filters.command('blacklist') & verify)
async def blacklist(client, message):
  data = await informations(client, message)
  if not data: 
     return
  chat_id, user_id, user_name = data
  add = await db.add_blacklist(user_id, int(chat_id))
  if not add:
    await message.reply_text(f"{user_name} already in blacklist")
  else:
    await message.reply_text(f"Successfully {user_name} Added to blacklist")
    
@Client.on_message(filters.command('rblacklist') & verify)
async def rblacklist(client, message):
  data = await informations(client, message)
  if not data: 
     return
  chat_id, user_id, user_name = data
  add = await db.remove_blacklist(user_id, int(chat_id))
  if not add:
    await message.reply_text(f"{user_name} not in blacklist")
  else:
    await message.reply_text(f"Successfully {user_name} removed from blacklist") 

@Client.on_message(filters.command('gblacklist') & verify)
async def get_all_blacklist(client, message):
  chat_type = message.chat.type
  if chat_type == "private":
     chat_id = await db.get_user_connection(str(message.from_user.id))
     if not chat_id:
        return await message.reply_text("I'm not connected to any groups!", quote=True)
  else:
     chat_id = message.chat.id
  msg = await message.reply_text("Processing.....")
  users = await db.get_chat_blacklists(int(chat_id))
  txt = "<b><u>blacklisted users are :-</b></u>\n\n"
  if users:
     async for user in users:
       try:
         k = await client.get_users(user['user_id'])
         txt+= f"<a href=tg://user?id={k.id}>{k.first_name}</a>\n"
       except IndexError:
         txt+= f"CHANNEL ({user['user_id']})"
  else:
     txt = "**No Blacklisted users in this Group**"
  return await msg.edit(txt)

@Client.on_message(filters.command('time') & verify)
async def time(client, message):
  chat_type = message.chat.type
  if chat_type == "private":
     chat_id = await db.get_user_connection(str(message.from_user.id))
     if not chat_id:
        return await message.reply_text("I'm not connected to any groups!", quote=True)
  else:
     chat_id = message.chat.id
  if len(message.command) == 1:
      return await message.reply_text("give me a time in seconds ! eg: /time 100")
  time = message.command[1]
  await save_settings(chat_id, "time", time)
  await message.reply_text(f"Successfully Time changed to **{time}s**")
  return 

async def informations(client, message):
  chat_type = message.chat.type
  if chat_type == "private":
     chat_id = await db.get_user_connection(str(message.from_user.id))
     if not chat_id:
        await message.reply_text("I'm not connected to any groups!", quote=True)
        return False
  else:
     chat_id = message.chat.id
  reply = message.reply_to_message
  if not reply:
    if len(message.command) == 1:
      await message.reply_text("give me a user id")
      return False
    user_id = message.command[1]
  else:
    if reply.sender_chat:
       user_id = reply.sender_chat.id
       user_name = reply.sender_chat.title
    else:
       user_id = reply.from_user.id
       user_name = reply.from_user.mention
  if not reply:
     try:
       user = await client.get_users(user_id)
       user_name = user.mention
     except IndexError:
       await message.reply("The given id is a channel ! please reply to channel message to add")
       return False 
     except PeerIdInvalid:
       await message.reply("This is an invalid user")
       return False
     except Exception as e:
       await message.reply(f'Error - {e}')
       return False
  return (chat_id, user_id, user_name) 
