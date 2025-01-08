from .. import *
from pyrogram import *
import aiofiles 

@app.on_message(filters.command('sh'))
async def sh(_, message):
  cmd = message.text.split(None, 1)[1]
  if len(message.command) < 2:
    return await message.reply("Text too short")
  results = await run(cmd)
  if len(results) > 4000:
    async with aiofiles.open('shell.txt', mode='w') as uwu:
      await uwu.write(results)
    await message.reply_document('shell.txt')
  else:
    await message.reply(f"```python\n{results}```")
