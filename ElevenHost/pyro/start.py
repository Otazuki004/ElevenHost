from ElevenHost import *
from pyrogram import *
from ElevenHost.api import *
from pyrogram import filters
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton 
import logging 

@app.on_message(filters.command('start'))
async def start(_, message):
    if not await api.exists(message.from_user.id):
        a = await message.reply("Registering you...")
        await api.create_user(message.from_user.first_name, message.from_user.id)
        await a.delete()
    # ------------------------------------------------
    await message.reply_photo(photo="https://i.imgur.com/rAGtzwy.jpeg", caption="| 𝗘𝗟𝗘𝗩𝗘𝗡 𝗛𝗢𝗦𝗧 |\n\n🍃 We provide the most reliable 🧡 and high-performance 🌩️ hosting solutions with a focus on simplicity and ease of use.\nEnjoy fast and secure hosting with unlimited potential! 🗝️ (°ᴗ°) 🥀✨\n\n🦋 Channel: @ElevenHost\n👾 Support: @ElevenHostSupport", reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton("Heya", callback_data="heya")]]))
