import time
import asyncio 
import time_formatter
from database import db 
from configs import temp 
from bot.main import Bot 
from pyrogram import filters 
from Mdmovies import time_formatter
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton

start_time = time.time()
BUTTON = [[InlineKeyboardButton("◀ back", callback_data="back")]]
START_MSG = "Hi {},\nI am a **auto delete bot** to delete messages from **bot and users** in your group after a specific time **(default 5 min)**. just add me to your group and make me admin with full permissions.\nconfigure me in group using /settings\n\n**For know more press help button**"
ABOUT_TXT = """
╔════❰ ᴍᴅ ғɪʟᴇ sᴛᴏʀᴇ ʙᴏᴛ ❱═❍⊱❁۪۪
║╭━━━━━━━━━━━━━━━➣
║┣⪼📃ʙᴏᴛ : [ᴀᴜᴛᴏ ᴅᴇʟᴇᴛᴇ ʙᴏᴛ](https://t.me/{})
║┣⪼👦ᴄʀᴇᴀᴛᴏʀ : [ᴍᴅᴀᴅᴍɪɴ](https://t.me/mdadmin2)
║┣⪼📡ʜᴏsᴛᴇᴅ ᴏɴ : ʜᴇʀᴏᴋᴜ
║┣⪼🗣️ʟᴀɴɢᴜᴀɢᴇ : ᴘʏᴛʜᴏɴ3
║┣⪼📚ʟɪʙʀᴀʀʏ : ᴘʏʀᴏɢʀᴀᴍ ᴀsʏɴᴄɪᴏ 1.13.0 
║┣⪼🕛ᴜᴘᴛɪᴍᴇ : {}
║┣⪼🗒️ᴠᴇʀsɪᴏɴ : 0.0.1
║╰━━━━━━━━━━━━━━━➣
╚══════════════════❍⊱❁۪۪
"""

@Bot.on_message(filters.command('start') & filters.private)
async def start(bot, cmd):
    buttons = [[InlineKeyboardButton('➕ Add Me To Your Groups ➕', url=f'http://t.me/{temp.B_NAME}?startgroup=true')],[InlineKeyboardButton('ℹ️ Help', callback_data='help'),InlineKeyboardButton('📢 update channel', url='https://t.me/venombotupdates')]]
    await cmd.reply(START_MSG.format(cmd.from_user.mention), reply_markup = InlineKeyboardMarkup(buttons))
    if await db.add_user(cmd.from_user.id, cmd.from_user.first_name):
        await bot.send_message(temp.LOG_CHANNEL, f"#NEWUSER: \nName - [{cmd.from_user.first_name}](tg://user?id={cmd.from_user.id})\nID - {cmd.from_user.id}")

@Bot.on_callback_query(filters.regex(r"^help"))
async def help(bot, query):
    HELP = "Add me to your group and make me admin with full permissions. use /settings to configure me in group\n\n**🗣️ Available commands :-**\n<code>/deleteall - To delete all messages in chat\n/Time - set deletion time\n/whitelist - To add users to whitelist\n/rwhitelist - To remove users from whitelist\n/blacklist - To add users to blacklist\n/rblacklist - to remove users from blacklist</code>\n\n**Four Deletion Mode Available.**\n**1. All messages** - delete all message after specific time\n**2. Except whitelist** - All messages except those messages from whitelisted users will be deleted.\n**3. blacklisted users** - only delete messages from blacklisted users\n**4. Except Bots** - All messages except those messages from bot will be deleted \n\n/createownbot - To create your own bot (paid 300₹)"
    await query.message.edit_text(text=HELP, reply_markup = InlineKeyboardMarkup(BUTTON))
 
@Bot.on_callback_query(filters.regex(r"^back"))
async def back(bot, query):
    buttons = [[InlineKeyboardButton('➕ Add Me To Your Groups ➕', url=f'http://t.me/{temp.B_NAME}?startgroup=true')],[InlineKeyboardButton('ℹ️ Help', callback_data='help'),InlineKeyboardButton('📢 update channel', url='https://t.me/venombotupdates')]]
    await query.message.edit_text(START_MSG.format(query.from_user.mention), reply_markup = InlineKeyboardMarkup(buttons))

@Bot.on_message(filters.command('createownbot') & filters.private)
async def create(bot, msg):
    await msg.reply_text("Contact [Owner](https://t.me/mdadmin2) to create your own **auto delete bot**")

@Bot.on_message(filters.command('about') & filters.private)
async def about(bot, msg):
   await msg.reply_text(text=ABOUT_TXT.format(temp.B_NAME, time_formatter(time.time() - start_time)), reply_markup=InlineKeyboardMarkup(BUTTON))
    
@Bot.on_message(filters.command('stats') & filters.private)
async def bot_stats(bot, msg):
    rju = await msg.reply('Fetching stats..')
    total_users = await db.total_users_count()
    total_chats = await db.total_chat_count()
    total_srv_chats = await db.total_served_chat()
    await rju.edit(f"★ Total users: <code>{total_users}</code>\n★ Total chats: <code>{total_chats}</code>\n★ Total served chats: <code>{total_srv_chats}</code>")
                                     
