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
   sucessful = 0
   MSG_ID = []
   MSG_ID.append({"first msg id": froms})
   try:
        k = await bot.get_messages(chat, froms)
   except:
        return await message.reply('Make Sure That Iam An Admin In The group, if group is private')
   if k.empty:
        return await message.reply('This may be group and iam not a admin of the group.')
   start_time = time.time()
   msg = await message.reply_text("Deleting all message **Please wait**")
   async for messages in bot.USER.iter_messages(chat, froms, 0):# int(froms), 100):
         current += 1
         if current % 20 == 0:
             await msg.edit_text(
                   text=f"Total messages : {current}\ndelete sucessful : {sucessful}\ndelete unsucessful : {error}\nalready deleted : {deleted}")
         if messages.empty:
               deleted+=1
               continue 
         try:
            msg_id = int(messages.message_id)
            if msg_id == int(msg.message_id):
               continue
            await bot.USER.delete_messages(chat, msg_id)
            MSG_ID.append(messages.message_id)
            sucessful+=1
         except Exception as e:
            print(e)
            error+=1
            continue
           
   time_taken = datetime.timedelta(seconds=int(time.time()-start_time))
   try:
     await bot.send_message(chat, text=f"ids\n{MSG_ID}")
   except:
      print(MSG_ID)
   await msg.edit(f"**completed**\n complete in : {time_taken}\nTotal messages : {current}\ndelete sucessful : {sucessful}\ndelete unsucessful : {error}\n\nalready deleted : {deleted}")
         
       
         
