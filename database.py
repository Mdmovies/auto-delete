from os import environ
import motor.motor_asyncio

DATABASE = environ.get("DATABASE")

class Database:

    def __init__(self, uri, database_name):
        self._client = motor.motor_asyncio.AsyncIOMotorClient(uri)
        self.db = self._client[database_name]
        self.col = self.db.users
        self.grp = self.db.groups
        self.srv = self.db.chats
        self.wht = self.db.whitelist
        self.blk = self.db.blacklist
        self.con = self.db.connection
        
    def new_user(self, id, name):
        return dict(
            id = id,
            name = name,
            )
    def new_group(self, id, title):
        return dict(
            id = id,
            title = title,
          )
        
    async def add_user(self, id, name):
        exist = await self.col.find_one({'id':int(id)})
        if not exist:
           user = self.new_user(id, name)
           return await self.col.insert_one(user)
        return False
    
    
    async def total_users_count(self):
        count = await self.col.count_documents({})
        return count 
      
    async def get_all_users(self):
        return self.col.find({})
    
    async def total_chat_count(self):
        count = await self.grp.count_documents({})
        return count
    

    async def get_all_chats(self):
        return self.grp.find({})


    async def get_db_size(self):
        return (await self.db.command("dbstats"))['dataSize']

    async def add_chat(self, chat, title):
        chats = await self.grp.find_one({'id':int(chat)})
        if not chats:
           chat = self.new_group(chat, title)
           return await self.grp.insert_one(chat)
        return False
    
    async def update_settings(self, id, settings):
        await self.grp.update_one({'id': int(id)}, {'$set': {'config': settings}})
        
    
    async def get_settings(self, id):
        default = {
            "auto_delete": True,
            "delete": True,
            "admins": True,
            "files": False,
            "link": False,
            "time": 300,
            "mode": "delete",
            "bots": True,
            "gifs": True,
            "photo": True,
            "video": True,
            "emoji": True,
            "polls": True,
            "voice": True,
            "audio": True,
            "files": True,
            "sticker": True
        }
        chat = await self.grp.find_one({'id':int(id)})
        if chat:
           returnchat.get('config', default)
        return default 
    
    async def get_served_chats(self):
       chats = self.srv.find({})
       s_chats = [chat['chat_id'] async for chat in chats]
       return s_chats
    
    async def is_served_chat(self, chat_id: int) -> bool:
       chat = await self.srv.find_one({"chat_id": chat_id})
       if not chat:
           return False
       return True

    async def add_served_chat(self, chat_id: int):
       is_served = await self.is_served_chat(chat_id)
       if is_served:
         return
       return await self.srv.insert_one({"chat_id": chat_id})
    
    async def remove_served_chat(self, chat_id: int):
       is_served = await self.is_served_chat(chat_id)
       if not is_served:
          return
       return await self.srv.delete_one({"chat_id": chat_id})
    
    async def total_served_chat(self):
       count = await self.srv.count_documents({})
       return count 
    
    async def in_whitelist(self, user: int, chat: int) -> bool:
       chat = await self.wht.find_one({"chat_id": chat, "user_id": user})
       return bool(chat)
    
    async def add_whitelist(self, user:int, chat_id: int):
       is_served = await self.in_whitelist(user, chat_id)
       if is_served:
         return False
       return await self.wht.insert_one({"chat_id": chat_id, "user_id": user})
    
    async def remove_whitelist(self, user:int, chat_id: int):
       is_served = await self.in_whitelist(user, chat_id)
       if not is_served:
         return False
       return await self.wht.delete_one({"chat_id": chat_id, "user_id": user})
    
    async def get_chat_whitelists(self, chat_id: int):
        return self.wht.find({"chat_id": chat_id})
    
    async def in_blacklist(self, user: int, chat: int) -> bool:
       chat = await self.blk.find_one({"chat_id": chat, "user_id": user})
       return bool(chat)
    
    async def add_blacklist(self, user:int, chat_id: int):
       is_served = await self.in_blacklist(user, chat_id)
       if is_served:
         return False
       return await self.blk.insert_one({"chat_id": chat_id, "user_id": user})
    
    async def remove_blacklist(self, user:int, chat_id: int):
       is_served = await self.in_blacklist(user, chat_id)
       if not is_served:
         return False
       return await self.blk.delete_one({"chat_id": chat_id, "user_id": user})
    
    async def get_chat_blacklists(self, chat_id: int):
       return self.blk.find({"chat_id": chat_id})
    
    async def in_connection(self, user: int, chat: int) -> bool:
       chat = await self.con.find_one({"chat_id": chat, "user_id": user})
       return bool(chat)
    
    async def add_connection(self, user:int, chat_id: int):
       is_served = await self.in_connection(user, chat_id)
       if is_served:
         return False
       return await self.con.insert_one({"chat_id": chat_id, "user_id": user})
    
    async def remove_connection(self, user:int, chat_id: int):
       is_served = await self.in_connection(user, chat_id)
       if not is_served:
         return False
       return await self.con.delete_one({"chat_id": chat_id, "user_id": user})
    
    async def get_user_connection(self, user_id: int):
       chat = await self.con.find_one({"user_id": user_id})
       return False if not chat else chat.get("chat_id")
    
db= Database(DATABASE, "auto-delete-bot")
