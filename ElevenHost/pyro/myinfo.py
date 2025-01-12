from ElevenHost import app
from .. import api
from pyrogram import filters

@app.on_message(filters.command("myinfo"))
async def myinfo_command(client, message):
    user_id = message.from_user.id
    user_info = await api.user_info(user_id)
    
    coins = user_info.get('coins', 0)
    name = user_info.get('name', 'Unknown')
    projects = user_info.get('projects', 0)
    github = user_info.get('git', 'Not Linked')
    
    user_info_text = f"""
✨ **ᴜsᴇʀ ᴘʀᴏғɪʟᴇ:**  
┌─────────────  
🎭 **Name:** {name}  
🆔 **ID:** `{user_id}`  
💰 **Coins:** `{coins}`  
📂 **Projects:** `{projects}`  
🌐 **GitHub:** `{github}`  
└─────────────"""

    await message.reply_text(user_info_text)
