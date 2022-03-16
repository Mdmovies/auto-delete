import asyncio 
from database import db 
from configs import temp 
from bot.main import Bot 
from pyrogram import filters 
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton

START_MSG = "hi {},\nI am a auto delete bot to delete messages in group after a specific time\nfor know more press help button"
buttons = [[InlineKeyboardButton('➕ Add Me To Your Groups ➕', url=f'http://t.me/{temp.B_NAME}?startgroup=true')],[InlineKeyboardButton('ℹ️ Help', callback_data='help')],[InlineKeyboardButton('📢 Support channel', callback_data='help')]]
            
@Bot.on_message(filters.command('start') & filters.private)
async def start(bot, cmd):
    await cmd.reply(START_MSG.format(cmd.from_user.mention), reply_markup = InlineKeyboardMarkup(buttons))
    if await db.add_user(cmd.from_user.id, cmd.from_user.first_name):
        await bot.send_message(temp.LOG_CHANNEL, f"#NEWUSER: \nName - [{cmd.from_user.first_name}](tg://user?id={cmd.from_user.id})\nID - {cmd.from_user.id}")

@Bot.on_callback_query(filters.regex(r"^help"))
async def help(bot, query):
    HELP = "CHANGE SOON"
    button = [[InlineKeyboardButton("◀️ back", callback_data="back")]]
    await query.message.edit_text(text=HELP, reply_markup = InlineKeyboardMarkup(button))
    
@Bot.on_callback_query(filters.regex(r"^back"))
async def back(bot, query):
    await query.message.edit_text(START_MSG.format(cmd.from_user.mention), reply_markup = InlineKeyboardMarkup(buttons))
