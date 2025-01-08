import io
from pyrogram import *
from ElevenHost import app
import traceback
from subprocess import getoutput as run
from pyrogram.enums import ChatAction

@app.on_message(filters.command(["logs", "log"]))
async def logs(_, message):
    if message.from_user.id == OWNER_ID or message.from_user.id in CO_OWNER_ID:
        print("")
    else:
        return
    run_logs = run("tail log.txt")
    text = await message.reply_text("`Getting logs...`")
    await bot.send_chat_action(message.chat.id, ChatAction.TYPING)
    await message.reply_text(f"```shell\n{run_logs}```")
    await text.delete()


@app.on_message(filters.command(["flogs", "flog"], prefixes=prefix))
async def logs(_, message):
    if message.from_user.id == OWNER_ID or message.from_user.id in CO_OWNER_ID:
        print("")
    else:
        return
    run_logs = run("cat log.txt")
    text = await message.reply_text("`Sending Full logs...`")
    await bot.send_chat_action(message.chat.id, ChatAction.UPLOAD_DOCUMENT)
    with io.BytesIO(str.encode(run_logs)) as logs:
        logs.name = "log.txt"
        await message.reply_document(
            document=logs,
        )
    await text.delete()
