import time
import asyncio 
import datetime
from typing import List 
from configs import temp
from pyrogram import filters 
from bot.main import User, Bot
from pyrogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from pyrogram.errors.exceptions.forbidden_403 import MessageDeleteForbidden

TG_MAX_SEL_MESG = 99
TG_MIN_SEL_MESG = 0

async def get_messages(
    bot: Bot,
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
    async for msg in User.iter_history(
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
    k = await Bot.get_chat(chat_id)
    await status.edit("sucessfully deleted all messages ✔️")
    await Bot.send_message(temp.LOG_CHANNEL, f"**sucessfully deleted all message in {k.title}**\nTime taken : {time_taken}\ncompleted : {total}\ndeleted : {delete}\nerror : {total - delete}")
    return True 
   
async def mass_delete_messages(
    client: Bot,
    chat_id: int,
    message_ids: List[int]
):
    try:
      await client.delete_messages(
         chat_id=chat_id,
         message_ids=message_ids,
         revoke=True)
    except MessageDeleteForbidden:
      await client.send_message(chat_id, "please give me admin permission **Delete messages** to delete messages")
    return

@Bot.on_message(filters.command(["deleteall", "delete"]) & filters.group)
async def delete_all(bot, message):
   msg = await message.reply_text("please wait it take some time to finish")
   await get_messages(
        bot,
        message.chat.id,
        0,
        msg.message_id if msg else message.message_id,
        [],
        msg
    )
   return
