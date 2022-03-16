import asyncio
import logging
from pyrogram import Client, __version__
from database import db
from pyrogram.raw.all import layer
from configs import temp
logging.basicConfig(level=logging.DEBUG,
                    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)
logging.getLogger("pyrogram").setLevel(logging.WARNING)


User = Client(session_name=temp.SESSION,
              api_id=temp.API_ID,
              api_hash=temp.API_HASH,
              workers=300
              )

Bot = Client(session_name="auto-deletes",
             api_id=temp.API_ID,
             api_hash=temp.API_HASH,
             bot_token=temp.BOT_TOKEN,
             plugins={"root": "bot/command"},
             sleep_threshold=5,
             workers=300
             )

async def start():
   chats = await db.get_served_chats()
   temp.GROUPS = chats 
   logging.info(f"Sucessfully updated {len(chats)} active Chats")
   await User.start()
   me = await User.get_me()
   temp.user_id = me.id
   logging.info(f" User bot ({me.username}) started")
   await Bot.start()
   me = await self.get_me()
   temp.bot_id = me.id
   logging.info(f"{me.first_name} with for Pyrogram v{__version__} (Layer {layer}) started on {me.username}.")
   temp.Bot = Bot 
   temp.User = User
   await idle()
   await Bot.stop()
   await User.stop()
   logging.info("Bot and user stopped. Bye.")
  
loop = asyncio.get_event_loop()
loop.run_until_complete(start_bot())
