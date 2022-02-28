import logging
from pyrogram import Client, __version__
from pyrogram.raw.all import layer
from config import SESSION, API_ID, API_HASH, BOT_TOKEN, GROUPS
logging.basicConfig(level=logging.DEBUG,
                    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)
logging.getLogger("pyrogram").setLevel(logging.WARNING)

BOT_ID = None

class Bot(Client):

    def __init__(self):
        super().__init__(
            session_name=SESSION,
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
        BOT_ID = me.id
        self.username = '@' + me.username
        logging.info(f"{me.first_name} with for Pyrogram v{__version__} (Layer {layer}) started on {me.username}.")
        
    async def stop(self, *args):
        await super().stop()
        logging.info("Bot stopped. Bye.")


app = Bot()
app.run()
        
