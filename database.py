import motor.motor_asyncio
from configs import DATABASE

class Database:

    def __init__(self, uri, database_name):
        self._client = motor.motor_asyncio.AsyncIOMotorClient(uri)
        self.db = self._client[database_name]
        self.col = self.db.users
        self.grp = self.db.groups
        self.srv = self.db.chats
        
    def new_user(self, id, name):
        return dict(
            id = id,
            name = name,
            )
    def new_group(self, id, title):
        return dict(
            id = id,
            title = title,
            config=dict(
              auto_delete=True,
              delete=True,
              admins=False,
              files=False,
              link=False,
              time=3600,
              mode=True,
              bots=True,
            ),
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
            "admins": False,
            "files": False,
            "link": False,
            "time": True,
            "mode": True,
            "bots": True,
        }
        chat = await self.grp.find_one({'id':int(id)})
        if chat:
            return chat.get('config', default)
        return default 
    
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
    
db= Database(DATABASE, "auto-delete-bot")
