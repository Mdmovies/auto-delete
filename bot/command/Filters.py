import asyncio 
from database import db 
from pyrogram import filters 
from bot.main import Bot as Client
from .command import save_settings 
from pyrogram.errors.exceptions.bad_request_400 import PeerIdInvalid

@Client.on_message(filters.command('whitelist') & filters.group)
async def whitelist(client, message):
  chat = message.chat.id
  if not message.reply_to_message:
    if len(message.command) == 1:
      return await message.reply_text("give me a user id")
    user_id = message.command[1]
  else:
    user_id = message.reply_to_message.from_user.id
  try:
     user = await client.get_users(user_id)
  except PeerIdInvalid:
        return await message.reply("This is an invalid user")
  except Exception as e:
        return await message.reply(f'Error - {e}')
  add = await db.add_whitelist(user_id, chat)
  if not add:
    await message.reply_text(f"{user.mention} already in whitelist")
  else:
    await message.reply_text(f"Successfully Added {user.mention} to whitelist")
    
@Client.on_message(filters.command('rwhitelist') & filters.group)
async def rwhitelist(client, message):
  chat = message.chat.id
  if not message.reply_to_message:
    if len(message.command) == 1:
      return await message.reply_text("give me a user id")
    user_id = message.command[1]
  else:
    user_id = message.reply_to_message.from_user.id
  try:
     user = await client.get_users(user_id)
  except PeerIdInvalid:
        return await message.reply("This is an invalid user")
  except Exception as e:
        return await message.reply(f'Error - {e}')
  add = await db.remove_whitelist(user_id, chat)
  if not add:
    await message.reply_text(f"{user.mention} not in whitelist")
  else:
    await message.reply_text(f"Successfully {user.mention} removed from whitelist")
    
@Client.on_message(filters.command('blacklist') & filters.group)
async def blacklist(client, message):
  chat = message.chat.id
  if not message.reply_to_message:
    if len(message.command) == 1:
      return await message.reply_text("give me a user id")
    user_id = message.command[1]
  else:
    user_id = message.reply_to_message.from_user.id
  try:
     user = await client.get_users(user_id)
  except PeerIdInvalid:
        return await message.reply("This is an invalid user")
  except Exception as e:
        return await message.reply(f'Error - {e}')
  add = await db.add_blacklist(user_id, chat)
  if not add:
    await message.reply_text(f"{user.mention} already in blacklist")
  else:
    await message.reply_text(f"Successfully {user.mention} Added to blacklist")
    
@Client.on_message(filters.command('rblacklist') & filters.group)
async def rblacklist(client, message):
  chat = message.chat.id
  if not message.reply_to_message:
    if len(message.command) == 1:
      return await message.reply_text("give me a user id")
    user_id = message.command[1]
  else:
    user_id = message.reply_to_message.from_user.id
  try:
     user = await client.get_users(user_id)
  except PeerIdInvalid:
        return await message.reply("This is an invalid user")
  except Exception as e:
        return await message.reply(f'Error - {e}')
  add = await db.remove_blacklist(user_id, chat)
  if not add:
    await message.reply_text(f"{user.mention} not in blacklist")
  else:
    await message.reply_text(f"Successfully {user.mention} removed from blacklist") 

@Client.on_message(filters.command('time') & filters.group)
async def time(client, message):
  chat = message.chat.id
  if len(message.command) == 1:
      return await message.reply_text("give me a time in seconds ! eg: /time 100")
  time = message.command[1]
  await save_settings(chat, "time", time)
  await message.reply_text(f"Successfully Time changed to **{time}s**")
  return
