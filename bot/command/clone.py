import os 
import sys
import time
import heroku3 
from pyrogram import Client as Bot, filters

TOKEN = "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" 

@Bot.on_message(filters.command('create') & filters.private)
async def create_clone(bot, message):
 try:
  app = {
     "region": "eu",
  }
  source_blob = {}
  overrides = {"env": {}}
  user = message.from_user
  cmd = message.command
  api_key, app_name = cmd[1], cmd[2]
  app_type = "production"
  domain = ".{0}.com".format(app_name)
  app["name"] = app_name
  git_name = "heroku_live"
  heroku_conn = heroku3.from_key(api_key)
  overrides["env"]["DJANGO_HOSTNAME"] = "{0}{1}".format(app_name, domain)
 # heroku_app = heroku_conn.app(app_name)
#  config = heroku_app.config()
  #source_blob["url"] = "https://api.github.com/repos/example/{0}/tarball/master?access_token={1}".format(
      #  app_name, TOKEN
 # )
  url = "https://github.com/Mdmovies/auto-delete"
  heroku_app = heroku_conn.create_app(name=app_name, region_id_or_name="eu")
  buid = heroku_app.create_build(url=url)
  source_blob["url"] = url
  data = {
        "app": app,
        "source_blob": source_blob,
        "overrides": overrides,
    }
  heroku_appsetup = heroku_conn.create_appsetup(**data)
  app = heroku_conn.app(heroku_appsetup.app.id)
  time_checkpoint = time.time
  waiting = True
  while True: 
      success, time_checkpoint = wait_for_status_event(heroku_conn, heroku_appsetup.id, time_checkpoint)
      if success:
          break 
  appsetup = heroku_conn.get_appsetup(heroku_appsetup.id)
  if appsetup.status == "succeeded":
      print("Enabling heroku labs runtime dyno metrics")
      app.enable_feature("runtime-dyno-metadata")
      await message.reply("dyno enabled")
 except Exception as e:
  await message.reply(e)
  
def wait_for_status_event(heroku_conn, appsetup_id, time_checkpoint):
    time_check = time.time()
    if (time_check - time_checkpoint) > 5:
        time_checkpoint = time_check
        print("checking status", end="\r")
        appsetup = heroku_conn.get_appsetup(appsetup_id)
        if appsetup.build:
            print("Build Available", appsetup.build)
            return True, time_checkpoint
        if appsetup.status in ["failed", "succeeded"]:
            return True, time_checkpoint
    return False, time_checkpoint
