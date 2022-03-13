import time
import asyncio 
import datetime
from bot.main import User, Bot
from pyrogram import Client, filters 
from pyrogram.types import InlineKeyboardButton, InlineKeyboardMarkup

@Client.on_message(filters.command(["del", "delete"]) & filters.group)
async def delete_all(bot, message):
   chat = message.chat.id
   froms = message.message_id
   total = 0
   error = 0
   current = 0
   deleted = 0
   sucessfull = 0
   start_time = time.time()
   msg = await message.reply_text("Deleting all message **Please wait**")
   async for message in bot.iter_messages(chat, froms, 0):
         current += 1
         if current % 20 == 0:
             await msg.edit_text(
                   text=f"Total messages : {current}\ndelete sucessful : {sucessful}\ndelete unsucessful : {error}\nalready deleted : {deleted}")
         if message.empty:
               deleted+=1
               continue 
         try:
            await bot.delete_messages(chat, message.message_id)
         except:
            error+=1
            continue
           
   time_taken = datetime.timedelta(seconds=int(time.time()-start_time))
   await msg.edit(f"**completed**\n complete in : {time_taken}\nTotal messages : {current}\ndelete sucessful : {sucessful}\ndelete unsucessful : {error}\n\nalready deleted : {deleted}")
         
       
         
