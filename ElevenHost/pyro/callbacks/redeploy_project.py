from ElevenHost import app
from pyrogram import filters
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from ElevenHost import *
import logging


@app.on_callback_query(filters.regex("^redeploy_"))
async def redeploy_project(_, callback_query):
    try:
        user_id = callback_query.from_user.id
        data = callback_query.data.split("_")
        project_id = int(data[1])
        callback_user_id = data[2]

        if str(user_id) != callback_user_id:
            return await callback_query.answer("❌ This action is not authorized for you!", show_alert=True)

        project_details = await api.project_info(user_id, project_id)
        if not project_details:
            return await callback_query.answer("❌ Unable to fetch project details or unauthorized action.", show_alert=True)

        await callback_query.message.edit_text(
            "♻️ **Redeploying your project. Please wait...**"
        )

        success = await api.host(user_id, project_id)
        if success:
            logs = await api.get_logs(user_id, project_id)
            log_text = logs[-400:] if logs else "No logs available for this project."

            await callback_query.message.edit_text(
                f"✅ **Project Redeployed Successfully!**\n\n"
                f"🔹 **Name:** {project_details.get('name', 'Unknown')}\n"
                f"🔹 **ID:** {project_id}\n"
                f"🔹 **Status:** 🟢 Alive\n\n"
                f"📜 **Logs:**\n<pre>{log_text}</pre>",
                reply_markup=InlineKeyboardMarkup([
                    [InlineKeyboardButton("🔃 Refresh", callback_data=f"refresh_{project_id}_{user_id}")],
                    [InlineKeyboardButton("⛔ Stop", callback_data=f"stop_{project_id}_{user_id}")]
                ])
            )
        else:
            await callback_query.message.edit_text(
                "❌ **Failed to redeploy the project. Please try again later or contact support.**"
            )
    except Exception as e:
        logging.error(f"Error in redeploy_project callback: {e}")
        await callback_query.answer(
            "🚨 An unexpected error occurred. Please try again later.",
            show_alert=True
        )
