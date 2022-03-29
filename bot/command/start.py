import asyncio 
from database import db 
from configs import temp 
from bot.main import Bot 
from pyrogram import filters 
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton

START_MSG = "Hi {},\nI am a **auto delete bot** to delete messages from **bot and users** in your group after a specific time. just add me to your group and make me admin with full permissions.\nconfigure me in group using /settings\n\n**For know more press help button**"
  
@Bot.on_message(filters.command('start') & filters.private)
async def start(bot, cmd):
    buttons = [[InlineKeyboardButton('➕ Add Me To Your Groups ➕', url=f'http://t.me/{temp.B_NAME}?startgroup=true')],[InlineKeyboardButton('ℹ️ Help', callback_data='help'),InlineKeyboardButton('📢 update channel', url='https://t.me/venombotupdates')]]
    await cmd.reply(START_MSG.format(cmd.from_user.mention), reply_markup = InlineKeyboardMarkup(buttons))
    if await db.add_user(cmd.from_user.id, cmd.from_user.first_name):
        await bot.send_message(temp.LOG_CHANNEL, f"#NEWUSER: \nName - [{cmd.from_user.first_name}](tg://user?id={cmd.from_user.id})\nID - {cmd.from_user.id}")

@Bot.on_callback_query(filters.regex(r"^help"))
async def help(bot, query):
    HELP = "Add me to your group and make me admin with full permissions. use /settings to configure me in group\n\n**🗣️ Available commands :-**\n<code>/deleteall - To delete all messages in chat\n/Time - set deletion time\n/whitelist - To add users to whitelist\n/rwhitelist - To remove users from whitelist\n/blacklist - To add users to blacklist\n/rblacklist - to remove users from blacklist</code>\n\n**Four Deletion Mode Available.**\n**1. All messages** - delete all message after specific time\n**2. Except whitelist** - All messages except those messages from whitelisted users will be deleted.\n**3. blacklisted users** - only delete messages from blacklisted users\n**4. Except Bots** - All messages except those messages from bot will be deleted \n\n/createownbot - To create your own bot (paid 300₹)"
    button = [[InlineKeyboardButton("◀ back", callback_data="back")]]
    await query.message.edit_text(text=HELP, reply_markup = InlineKeyboardMarkup(button))
    
@Bot.on_callback_query(filters.regex(r"^back"))
async def back(bot, query):
    buttons = [[InlineKeyboardButton('➕ Add Me To Your Groups ➕', url=f'http://t.me/{temp.B_NAME}?startgroup=true')],[InlineKeyboardButton('ℹ️ Help', callback_data='help'),InlineKeyboardButton('📢 update channel', url='https://t.me/venombotupdates')]]
    await query.message.edit_text(START_MSG.format(query.from_user.mention), reply_markup = InlineKeyboardMarkup(buttons))

@Bot.on_message(filters.command('createownbot') & filters.private)
async def create(bot, msg):
    await msg.reply_text("Contact [Owner](https://t.me/mdadmin2) to create your own **auto delete bot**")
