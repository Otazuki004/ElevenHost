from pyrogram import *
from ElevenHost import *
from pyrogram.types import *
from ElevenHost.others import *
import logging
import traceback 
import asyncio

@app.on_callback_query(filters.regex("^repo_"))
async def connect_repo(_, callback_query):
  try:
    user_id = callback_query.from_user.id
    data = callback_query.data.split("_")
    project_id = int(data[1])
    repo_id = int(data[2])

    success = await api.set_repo(user_id, project_id, repo_id)
    if success:
        await callback_query.message.edit_text("✅ Repository connected successfully!")
    else:
        await callback_query.answer("❌ Failed to connect the repository. Try again.", show_alert=True)
  except Exception as e:
    logging.error(f"Error in connect_repo callback: {e}")
    await callback_query.answer("🚨 An error occurred. Please try again later.", show_alert=True)
      
