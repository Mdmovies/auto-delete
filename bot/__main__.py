import asyncio
import logging 
from database import db
from configs import temp
from .main import Bot, User
from pyrogram.raw.all import layer
from pyrogram import Client, __version__, idle

logging.basicConfig(level=logging.DEBUG,
                    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)
logging.getLogger("pyrogram").setLevel(logging.WARNING)

async def start():
   chats = await db.get_served_chats()
   temp.GROUPS = chats 
   logging.info(f"Sucessfully updated {len(chats)} active Chats")
   await User.start()
   me = await User.get_me()
   temp.user_id = me.id
   temp.U_NAME = me.username
   logging.info(f" User bot ({me.username}) started")
   await Bot.start()
   me = await Bot.get_me()
   temp.bot_id = me.id
   temp.B_NAME = me.first_name
   logging.info(f"{me.first_name} with for Pyrogram v{__version__} (Layer {layer}) started on {me.username}.")
   temp.Bot = Bot 
   temp.User = User
   await idle()
   await Bot.stop()
   await User.stop()
   logging.info("Bot and user stopped. Bye.")
  
loop = asyncio.get_event_loop()
loop.run_until_complete(start())
