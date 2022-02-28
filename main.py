import logging
from pyrogram import Client, __version__
from database import db
from pyrogram.raw.all import layer
from config import SESSION, API_ID, API_HASH, BOT_TOKEN, GROUPS
logging.basicConfig(level=logging.DEBUG,
                    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)
logging.getLogger("pyrogram").setLevel(logging.WARNING)

 
class User(Client):
    def __init__(self):
        super().__init__(
            SESSION,
            api_hash=API_HASH,
            api_id=APP_ID,
            workers=4
        )
        
    async def start(self):
        await super().start()
        usr_bot_me = await self.get_me()
        return (self, usr_bot_me.id)

    async def stop(self, *args):
        await super().stop()
        logging.info("User Bot stopped. Bye.")
        
class Bot(Client):
    ID: int = None 
    USER: User = None
    USER_ID: int = None

    def __init__(self):
        super().__init__(
            session_name="auto-delete",
            api_id=API_ID,
            api_hash=API_HASH,
            bot_token=BOT_TOKEN,
            workers=50,
            plugins={"root": "bot"},
            sleep_threshold=5,
        )
        
    async def start(self):
        chats = await db.get_served_chats()
        GROUPS.append(chats)
        await super().start()
        me = await self.get_me()
        self.ID = me.id
        self.username = '@' + me.username
        logging.info(f"{me.first_name} with for Pyrogram v{__version__} (Layer {layer}) started on {me.username}.")
        self.USER, self.USER_ID = await User().start()
        
    async def stop(self, *args):
        await super().stop()
        logging.info("Bot stopped. Bye.")


app = Bot()
app.run()
        
