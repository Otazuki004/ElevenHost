from .. import *
from pyrogram import *
import aiofiles 

@app.on_message(filters.command('sh'))
async def sh(_, message):
  if len(message.command) < 2:
    return await message.reply("ᴄᴏᴅᴇ ɴᴏᴛ ғᴏᴜɴᴅ !")
  a = await message.reply("Processing...")
  cmd = message.text.split(None, 1)[1]
  results = await run(cmd) or "ɴᴏ ᴏᴜᴛᴘᴜᴛ"
  if len(results) > 4000:
    async with aiofiles.open('shell.txt', mode='w') as uwu:
      await uwu.write(results)
    await message.reply_document('shell.txt')
  else:
    await message.reply(f"<pre>{results}</pre>")
  await a.delete()
