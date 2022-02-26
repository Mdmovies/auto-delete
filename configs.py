from os import environ 

API_ID = int(environ.get("API_ID"))
API_HASH = environ.get("API_HASH")
BOT_TOKEN = environ.get("BOT_TOKEN")
DATABASE = environ.get("DATABASE")
SESSION = environ.get("SESSION")
LOG_CHANNEL = int(environ.get("LOG_CHANNEL"))
