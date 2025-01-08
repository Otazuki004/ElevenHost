# ©️ @ParadopiaXD | @YoursSage

import io
import sys
import traceback
from ElevenHost import app
from datetime import datetime
from pyrogram import filters
from pyrogram.types import Message

async def aexec(code, app, msg):
    exec(
        "async def __aexec(app, msg): "
        + "\n p = print"
        + "".join(f"\n {l_}" for l_ in code.split("\n"))
    )
    return await locals()["__aexec"](app, msg)
    
@app.on_message(filters.command("eval"))
@app.on_edited_message(filters.command("eval"))
async def runPyro_Funcs(app:app, msg:Message) -> None:
    code = msg.text.split(None, 1)
    if len(code) == 1:
        return await msg.reply("<sʏɴᴛᴀx ᴇʀʀᴏʀ> ᴄᴏᴅᴇ ɴᴏᴛ ғᴏᴜɴᴅ !")
    message = await msg.reply("ʀᴜɴɴɪɴɢ...")
    soac = datetime.now()
    osder = sys.stderr
    osdor = sys.stdout
    redr_opu = sys.stdout = io.StringIO()
    redr_err = sys.stderr = io.StringIO()
    stdout, stderr, exc = None, None, None
    try:
        vacue = await aexec(code[1], app, msg)
    except Exception:
        exc = traceback.format_exc()
    stdout = redr_opu.getvalue()
    stderr = redr_err.getvalue()
    sys.stdout = osdor
    sys.stderr = osder
    evason = exc or stderr or stdout or vacue or "ɴᴏ ᴏᴜᴛᴘᴜᴛ"
    eoac = datetime.now()
    runcs = (eoac - soac).microseconds / 1000
    oucode = f"📎 ᴄᴏᴅᴇ:\n<pre>{code[1]}</pre>\n📒 ᴏᴜᴛᴘᴜᴛ:\n<pre>{evason}</pre>\n✨ ᴛɪᴍᴇ ᴛᴀᴋᴇɴ: {runcs}ᴍɪʟɪsᴇᴄᴏɴᴅ"
    if len(oucode) > 10000000:
        await message.edit("⚠️ ᴏᴜᴛᴘᴜᴛ ᴛᴏᴏ ʟᴏɴɢ...")
    else:
        await message.edit(oucode)
