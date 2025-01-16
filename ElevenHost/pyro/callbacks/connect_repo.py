from pyrogram import *
from ElevenHost import *
from pyrogram.types import *
from ElevenHost.others import *
import logging
import traceback

@app.on_callback_query(filters.regex("^repo_"))
async def connect_repo(_, callback_query):
    try:
        data = callback_query.data.split("_")
        user_id = callback_query.from_user.id
        project_id = int(data[1])
        repo_id = int(data[2])
        if str(user_id) != data[3]:
            return await callback_query.answer("❌ This action is not authorized for you!", show_alert=True)

        success = await api.set_repo(user_id, project_id, repo_id)
        if success:
            await callback_query.message.edit_text("✅ **Repository connected successfully!**")
        else:
            await callback_query.answer("❌ Failed to connect the repository. Please try again.", show_alert=True)
    except Exception as e:
        logging.error(f"Error in connect_repo callback: {traceback.format_exc()}")
        await callback_query.answer("🚨 An error occurred. Please try again later.", show_alert=True)
