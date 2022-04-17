from database import db

SETTINGS = {}

async def get_settings(group):
  settings = SETTINGS.get(group)
  if not settings:
     settings = await db.get_settings(group)
     SETTINGS[group] = settings 
  return settings

async def save_settings(group, key, value):
  current = await get_settings(group)
  current[key] = value 
  SETTINGS[group] = current
  await db.update_settings(group, current)
  return
