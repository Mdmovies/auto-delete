import time
import asyncio 
import datetime 
from typing import List
from bot.main import User, Bot
from pyrogram import Client, filters 
from pyrogram.types import InlineKeyboardButton, InlineKeyboardMarkup

TG_MAX_SEL_MESG = 20
TG_MIN_SEL_MESG = 0

async def get_messages(
    client: Bot,
    chat_id: int,
    min_message_id: int,
    max_message_id: int,
    filter_type_s: List[str],
    status
):
    total = 0
    delete = 0
    messages_to_delete = []
    start_time = time.time()
    async for msg in client.iter_history(
        chat_id=chat_id,
        limit=None
    ):
        total+=1
        if (
            min_message_id <= msg.message_id and
            max_message_id >= msg.message_id
        ):
            if len(filter_type_s) > 0:
                for filter_type in filter_type_s:
                    obj = getattr(msg, filter_type)
                    if obj:
                        messages_to_delete.append(msg.message_id)
            else:
                if msg.message_id != status.message_id:
                    messages_to_delete.append(msg.message_id)
        feched = len(messages_to_delete)
        if feched > TG_MAX_SEL_MESG:
            await mass_delete_messages(
                Bot,
                chat_id,
                messages_to_delete
            )
            delete+=int(feched)
            messages_to_delete = []
            await status.edit(f"completed : {total}\ndeleted : {delete}\nerror : {total - delete}")
    unknown = len(messages_to_delete)
    if unknown > TG_MIN_SEL_MESG:
        await mass_delete_messages(
            Bot,
            chat_id,
            messages_to_delete
        )
        delete+=int(unknown)
        messages_to_delete = []
    time_taken = datetime.timedelta(seconds=int(time.time()-start_time))
    await status.edit(f"sucessful\nTime taken : {time_taken}\ncompleted : {total}\ndeleted : {delete}\nerror : {total - delete}")
    return True 
   
async def mass_delete_messages(
    client: Bot,
    chat_id: int,
    message_ids: List[int]
):
    return await client.delete_messages(
        chat_id=chat_id,
        message_ids=message_ids,
        revoke=True
    )
@Client.on_message(filters.command(["del", "delete"]) & filters.group)
async def delete_all(bot, message):
   msg = await message.reply_text("please wait it take some time to finish")
   await get_messages(
        bot.USER,
        message.chat.id,
        0,
        msg.message_id if msg else message.message_id,
        [],
        msg
    )
   return 

async def dumb(client, message):
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
           
   
   try:
     await bot.send_message(chat, text=f"ids\n{MSG_ID}")
   except:
      print(MSG_ID)
 #  await msg.edit(f"**completed**\n complete in : {time_taken}\nTotal messages : {current}\ndelete sucessful : {sucessful}\ndelete unsucessful : {error}\n\nalready deleted : {deleted}")
         
       
         
