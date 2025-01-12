from ElevenHost import app
from .. import api
from pyrogram import *

@app.on_message(filters.command("myinfo"))
async def myinfo_command(client, message):
    user_id = message.from_user.id
    user_info = await api.user_info(user_id)
    
    coins = user_info.get('coins', 0)
    name = user_info.get('name', 'Unknown')
    projects = user_info.get('projects', 0)
    
    user_info_text = f"""
 **🍃 ᴜsᴇʀ ɪɴғᴏ:**
    👤 **Name:** {name}
    🆔 **User ID:** {user_id}
    🪙 **Coins:** {coins}
    💼 **Projects:** {projects}"""

    return await message.reply_text(user_info_text)
