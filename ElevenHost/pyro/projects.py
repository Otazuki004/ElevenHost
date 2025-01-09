from ElevenHost import app
from pyrogram import filters, Client
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton 
from .. import *

@app.on_message(filters.command(["project", "projects"]))
async def projects(_, message):
    if not await api.exists(message.from_user.id): return await message.reply("You didn't registered please use /start to register!")
    buttons = [
        [InlineKeyboardButton("𝙋𝙍𝙊 𝙎𝙀𝙍𝙑𝙀𝙍", callback_data="2GB_RAM")],
        [InlineKeyboardButton("𝙎𝙐𝙋𝙀𝙍 𝙎𝙀𝙍𝙑𝙀𝙍", callback_data="4GB_RAM")],
        [InlineKeyboardButton("𝙐𝙇𝙏𝙍𝘼 𝙎𝙀𝙍𝙑𝙀𝙍", callback_data="6GB_RAM")],
        [InlineKeyboardButton("𝙐𝙇𝙏𝙄𝙈𝘼𝙏𝙀 𝙎𝙀𝙍𝙑𝙀𝙍", callback_data="8GB_RAM")],
        [InlineKeyboardButton("𝙇𝙀𝙂𝙀𝙉𝘿𝘼𝙍𝙔 𝙎𝙀𝙍𝙑𝙀𝙍", callback_data="16GB_RAM")],
        [InlineKeyboardButton("𝙂𝙊𝘿 𝙎𝙀𝙍𝙑𝙀𝙍", callback_data="32GB_RAM")]
    ]
    reply_markup = InlineKeyboardMarkup(buttons)
    await message.reply_photo(photo="http://ibb.co/cYwL2ZY", caption="𝗖𝗛𝗢𝗢𝗦𝗘 𝗔 𝗦𝗘𝗥𝗩𝗘𝗥", reply_markup=reply_markup)
