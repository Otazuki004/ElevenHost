from pyrogram import *
from ElevenHost import *
from pyrogram.types import *
from ElevenHost.others import *
import logging
import traceback 
import asyncio

@app.on_callback_query(filters.regex("^change_repo_"))
async def change_repo(_, callback_query):
  try:
    user_id = int(callback_query.from_user.id)
    project_id = int(callback_query.data.split("_")[2])
    if user_id != int(callback_query.data.split("_")[3]):
      return await callback_query.answer("This is not for you!")
    repos = await api.get_repos(user_id)
    if not repos:
      return await callback_query.answer("⚠️ No repositories found.", show_alert=True)
      
    buttons = [
      [InlineKeyboardButton(repo.get("name"), callback_data=f"repo_{project_id}_{repo.get('id')}")]
      for repo in repos
    ]
    buttons.append([InlineKeyboardButton("❌ Cancel", callback_data=f"cancel_change_repo_{project_id}")])

    await callback_query.message.edit_text(
      "🔄 **Select a repository to change to:**",
      reply_markup=InlineKeyboardMarkup(buttons)
    )
  except Exception as e:
    logging.error(f"Error in change_repo callback: {e}")
    await callback_query.answer("🚨 An error occurred. Please try again later.", show_alert=True)
