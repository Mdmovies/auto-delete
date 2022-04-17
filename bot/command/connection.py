import asyncio 
import logging
from database import db
from bot.main import Bot 
from configs import temp
from pyrogram import filters 

logger = logging.getLogger(__name__)
logger.setLevel(logging.ERROR)

@Bot.on_message((filters.private | filters.group) & filters.command('connect'))
async def addconnection(client, message):
    userid = message.from_user.id if message.from_user else None
    if not userid:
        return await message.reply(f"You are anonymous admin. Use /connect {message.chat.id} in PM")
    chat_type = message.chat.type

    if chat_type == "private":
        try:
            cmd, group_id = message.text.split(" ", 1)
        except:
            await message.reply_text(
                "<b>Enter in correct format!</b>\n\n"
                "<code>/connect <groupid></code>\n\n", quote=True)
            return 
    elif chat_type in ["group", "supergroup"]:
        group_id = message.chat.id

    try:
        st = await client.get_chat_member(group_id, userid)
        if (
                st.status != "administrator"
                and st.status != "creator"
                and userid not in temp.ADMINS
        ):
            await message.reply_text("You should be an admin in Given group!", quote=True)
            return
    except Exception as e:
        logger.exception(e)
        await message.reply_text(
            "Invalid Group ID!\n\nIf correct, Make sure I'm present in your group!!",
            quote=True,
        )

    try:
        st = await client.get_chat_member(group_id, "me")
        if st.status == "administrator":
            ttl = await client.get_chat(group_id)
            title = ttl.title
            
            conn = await db.add_connection(str(userid), str(group_id))
            if conn:
                await message.reply_text(
                    f"Successfully connected to **{title}**\nNow manage your group from my pm !",
                    quote=True,
                    parse_mode="md"
                )
                if chat_type in ["group", "supergroup"]:
                    await client.send_message(
                        userid,
                        f"Connected to **{title}** !",
                        parse_mode="md"
                    )
                    
            else:
                await message.reply_text(
                    "You're already connected to this chat!",
                    quote=True
                )
                
        else:
            await message.reply_text("Add me as an admin in group", quote=True)
    except Exception as e:
        logger.exception(e)
        await message.reply_text('Some error occurred! Try again later.', quote=True)
        return


@Bot.on_message((filters.private | filters.group) & filters.command('disconnect'))
async def deleteconnection(client, message):
    userid = message.from_user.id if message.from_user else None
    if not userid:
        return await message.reply(f"You are anonymous admin. Use /connect {message.chat.id} in PM")
    chat_type = message.chat.type

    if chat_type == "private":
        group_ids = await db.get_user_connection(str(user_id))
        if group_ids is None:
           return await message.reply_text("There are no chat connected to me!\nDo /connect to connect.", quote=True)
        group_id = group_ids['chat_id']
        
    elif chat_type in ["group", "supergroup"]:
        group_id = message.chat.id

    st = await client.get_chat_member(group_id, userid)
    if (
        st.status != "administrator"
        and st.status != "creator"
        and str(userid) not in temp.ADMINS
        ):
        return

    delcon = await db.remove_connection(str(userid), str(group_id))
    return await message.reply_text("Successfully disconnected from this chat", quote=True)
     
@Bot.on_message(filters.private & filters.command(["connections"]))
async def connections(client, message):
    userid = message.from_user.id
    groupid = await db.get_user_connection(str(userid))
    if groupid is None:
        await message.reply_text(
            "There are no active connections!! Connect to some groups first.",
            quote=True
        )
        return
    ttl = await client.get_chat(int(groupid['chat_id']))
    title = ttl.title
    await message.reply_text(f"Your current connected Group is\n\n{title} ({ttl.id})")
    return
