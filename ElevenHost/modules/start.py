from ElevenHost import *
from pyrogram import *
from ElevenHost.api import *

api = OneApi()

@app.on_message(filters.command('start'))
async def start(_, message):
  if await api.exists(message.from_user.id): pass
  else: # Welcome new users heHe
    await message.reply("hm looks like new user")
    return
  # ------------------------------------------------
  await message.reply("I know you before")
