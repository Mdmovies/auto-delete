import asyncio 
from database import db 
from pyrogram import Client, filters 

@Client.on_message(filters.command('whitelist') & filters.group)
async def whitelist(client, message):
  chat = message.chat.id
  if not message.reply_to_message:
    if message.text < 2:
      return await message.reply_text("give a user id")
    i, user_id = await message.split(None, 1)
  else:
    user_id = message.reply_to_message.from_user.id
  add = await db.add_whitelist(user_id, chat)
  if not add:
    await message.reply_text("given user already in whitelist")
  else:
    await message.reply_text(f"Added {user_id} to whitelist")
    
@Client.on_message(filters.command('rwhitelist') & filters.group)
async def rwhitelist(client, message):
  chat = message.chat.id
  if not message.reply_to_message:
    if message.text < 2:
      return await message.reply_text("give a user id")
    i, user_id = await message.split(None, 1)
  else:
    user_id = message.reply_to_message.from_user.id
  add = await db.remove_whitelist(user_id, chat)
  if not add:
    await message.reply_text("given user not in whitelist")
  else:
    await message.reply_text(f"{user_id} removed from whitelist")
    
@Client.on_message(filters.command('blacklist') & filters.group)
async def blacklist(client, message):
  chat = message.chat.id
  if not message.reply_to_message:
    if message.text < 2:
      return await message.reply_text("give a user id")
    i, user_id = await message.split(None, 1)
  else:
    user_id = message.reply_to_message.from_user.id
  add = await db.add_blacklist(user_id, chat)
  if not add:
    await message.reply_text("given user already in blacklist")
  else:
    await message.reply_text(f"Added {user_id} to blacklist")
    
@Client.on_message(filters.command('rblacklist') & filters.group)
async def rblacklist(client, message):
  chat = message.chat.id
  if not message.reply_to_message:
    if message.text < 2:
      return await message.reply_text("give a user id")
    i, user_id = await message.split(None, 1)
  else:
    user_id = message.reply_to_message.from_user.id
  add = await db.remove_blacklist(user_id, chat)
  if not add:
    await message.reply_text("given user not in blacklist")
  else:
    await message.reply_text(f"{user_id} removed from blacklist") 
