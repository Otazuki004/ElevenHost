from ElevenHost import app
from pyrogram import filters
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from .. import api
import logging


@app.on_callback_query(filters.regex("^refresh_"))
async def refresh_project(_, callback_query):
    try:
        user_id = callback_query.from_user.id
        project_id = int(callback_query.data.split("_")[1])
        
        project_details = await api.project_info(user_id, project_id)
        if not project_details:
            return await callback_query.answer("❌ Unable to fetch project details or unauthorized action.", show_alert=True)

        logs = await api.get_logs(user_id, project_id)
        log_text = logs if logs else "No logs available for this project."

        await callback_query.message.edit_text(
            f"🔄 **Project Details Refreshed!**\n\n"
            f"🔹 **Name:** {project_details.get('name', 'Unknown')}\n"
            f"🔹 **ID:** {project_id}\n"
            f"🔹 **Status:** 🟢 Alive\n\n"
            f"📜 **Logs:**\n{log_text}",
            reply_markup=InlineKeyboardMarkup([
                [InlineKeyboardButton("🔃 Refresh", callback_data=f"refresh_{project_id}")],
                [InlineKeyboardButton("⛔ Stop", callback_data=f"stop_{project_id}")]
            ])
        )
    except Exception as e:
        logging.error(f"Error in refresh_project callback: {e}")
        await callback_query.answer(
            "🚨 An unexpected error occurred. Please try again later.",
            show_alert=True
        )
