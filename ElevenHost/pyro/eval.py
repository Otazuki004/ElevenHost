# ©️ @Hyper_Speed0 & @ParadopiaxD

import io
import sys
import traceback
from ElevenHost import app
from datetime import datetime
from pyrogram import filters
from pyrogram.types import Message
import aiofiles

async def aexec(code, app, msg):
    m, from_user, r = msg, msg.from_user, msg.reply_to_message
    exec(
        "async def __otazuki_run(app, msg, m, r, frm): "
        + "\n p = print"
        + "".join(f"\n {l_}" for l_ in code.split("\n"))
    )
    return await locals()["__otazuki_run"](app, msg, m, r, from_user)
    
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
    oucode = f"📎 ᴄᴏᴅᴇ:\n```python\n{code[1]}```\n📒 ᴏᴜᴛᴘᴜᴛ:\n```python\n{evason}```\n✨ ᴛɪᴍᴇ ᴛᴀᴋᴇɴ: {runcs}ᴍs"
    if len(oucode) > 4000:
        async with aiofiles.open('eval.txt', mode='w') as f:
            await f.write(runcs)
        await message.reply_document('eval.txt')
    else:
        await message.edit(oucode)
