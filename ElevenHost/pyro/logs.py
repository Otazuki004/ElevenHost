from pyrogram import *
from ElevenHost import *

@app.on_message(filters.command(["logs", "log"]) & filters.user(DEVS))
async def logs(_, message):
  run_logs = await run("tail log.txt")
  await message.reply_text(f"```shell\n{run_logs}```")

@app.on_message(filters.command(["flogs", "flog"]) & filters.user(DEVS))
async def flogs(_, message):
  await message.reply_document(document='log.txt')
