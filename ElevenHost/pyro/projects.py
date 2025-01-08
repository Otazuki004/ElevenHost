from ElevenHost import app
from pyrogram import filters, Client
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton 
from variables import DEVS

@app.on_message(filters.command(["projects"]))
def start(client, message):
    if message.from_user.id in DEVS:
        buttons = [
            [InlineKeyboardButton("𝙋𝙍𝙊 𝙎𝙀𝙍𝙑𝙀𝙍", callback_data="2GB_RAM")],
            [InlineKeyboardButton("𝙎𝙐𝙋𝙀𝙍 𝙎𝙀𝙍𝙑𝙀𝙍", callback_data="4GB_RAM")],
            [InlineKeyboardButton("𝙐𝙇𝙏𝙍𝘼 𝙎𝙀𝙍𝙑𝙀𝙍", callback_data="6GB_RAM")],
            [InlineKeyboardButton("𝙐𝙇𝙏𝙄𝙈𝘼𝙏𝙀 𝙎𝙀𝙍𝙑𝙀𝙍", callback_data="8GB_RAM")],
            [InlineKeyboardButton("𝙇𝙀𝙂𝙀𝙉𝘿𝘼𝙍𝙔 𝙎𝙀𝙍𝙑𝙀𝙍", callback_data="16GB_RAM")],
            [InlineKeyboardButton("𝙂𝙊𝘿 𝙎𝙀𝙍𝙑𝙀𝙍", callback_data="32GB_RAM")]
        ]
        reply_markup = InlineKeyboardMarkup(buttons)
        message.reply_photo(photo="http://ibb.co/cYwL2ZY", caption="𝗖𝗛𝗢𝗢𝗦𝗘 𝗔 𝗦𝗘𝗥𝗩𝗘𝗥", reply_markup=reply_markup)
    else:
        message.reply_text("__**You Have Not Connected GitHub Yet. Please Connect it & Use Command Again.**__")

@app.on_callback_query()
def callback(client, callback_query):
    if callback_query.from_user.id in DEVS:
        data = callback_query.data
        app_info = ""
        if data == "2GB_RAM":
            app_info = "⬤ SERVER info:\n  ⬡ Name: 2 GB RAM\n  ⬡ Ram: 2 GB\n\n⬤ APP Status:\n  ⬡ Service: Offline\n  ⬡ Git: None"
        elif data == "4GB_RAM":
            app_info = "⬤ SERVER info:\n  ⬡ Name: 4 GB RAM\n  ⬡ Ram: 4 GB\n\n⬤ APP Status:\n  ⬡ Service: Offline\n  ⬡ Git: None"
        elif data == "6GB_RAM":
            app_info = "⬤ SERVER info:\n  ⬡ Name: 6 GB RAM\n  ⬡ Ram: 6 GB\n\n⬤ APP Status:\n  ⬡ Service: Offline\n  ⬡ Git: None"
        elif data == "8GB_RAM":
            app_info = "⬤ SERVER info:\n  ⬡ Name: 8 GB RAM\n  ⬡ Ram: 8 GB\n\n⬤ APP Status:\n  ⬡ Service: Offline\n  ⬡ Git: None"
        elif data == "16GB_RAM":
            app_info = "⬤ SERVER info:\n  ⬡ Name: 16 GB RAM\n  ⬡ Ram: 16 GB\n\n⬤ APP Status:\n  ⬡ Service: Offline\n  ⬡ Git: None"
        elif data == "32GB_RAM":
            app_info = "⬤ SERVER info:\n  ⬡ Name: 32 GB RAM\n  ⬡ Ram: 32 GB\n\n⬤ APP Status:\n  ⬡ Service: Offline\n  ⬡ Git: None"
        
        callback_query.message.delete()
        callback_query.message.reply_photo(photo="http://ibb.co/Cmv9stG", caption="𝗦 𝗘 𝗥 𝗩 𝗘 𝗥\n\n" + app_info)
    else:
        callback_query.answer("__**You Have Not Connected GitHub Yet. Please Connect it & Use Command Again.**__", show_alert=True)
