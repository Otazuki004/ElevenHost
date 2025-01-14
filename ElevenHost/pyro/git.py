from pyrogram import *
from .. import *
import httpx
from pyrogram.enums import ChatType
from pyrogram.types import *

@app.on_message(filters.command("git"))
async def git(_, message):
  if not message.chat.type == ChatType.PRIVATE: return await message.reply("This command only works in private")
  elif not await api.exists(message.from_user.id): return await message.reply("❌ You are not registered yet. Please use /start to register your account.")
  love = await message.reply("Loading...")
  user = await api.user_info(message.from_user.id)

  async with httpx.AsyncClient() as mano:
    response = await mano.get(f"https://api.github.com/users/{user.get('git')}")
    response = response.json()
    bio, followers, following = response.get('bio'), response.get('followers'), response.get('following')
  
  txt = f"""| 𝗚𝗜𝗧𝗛𝗨𝗕 |

Repo Allowed: {len((await api.get_repos(message.from_user.id) or []))}

Name: {user.get('git')}
Bio: {bio}
Followers: {followers}
Following: {following}"""
  btn = InlineKeyboardMarkup([[InlineKeyboardButton("Disconnect", callback_data=f"dis_github")]])
  await love.delete()
  await message.reply_photo("http://ibb.co/0nTck0T", caption=txt, reply_markup=btn)

@app.on_callback_query(filters.regex("dis_github"))
async def disconnect_git(_, query):
  user_id = query.from_user.id
  if not await api.exists(user_id): return await query.answer("❌ You are not registered yet. Please use /start to register your account.", show_alert=True)
  ohk = await api.disconnect_git(user_id)
  if ohk:
    await query.message.delete()
    await app.send_message(query.message.chat.id, "Successfully disconnected your github.")
  else:
    await query.message.edit("Failed to disconnect your GitHub")
