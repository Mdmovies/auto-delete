from configs import temp
from pyrogram import Client

User = Client(session_name=temp.SESSION,
              api_id=temp.API_ID,
              api_hash=temp.API_HASH,
              password=temp.PASSWORD,
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
