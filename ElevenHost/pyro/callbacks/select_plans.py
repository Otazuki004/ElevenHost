from pyrogram import *
from ElevenHost import *
from pyrogram.type import *
from ElevenHost.others import *
import logging
import traceback 
import asyncio

@app.on_callback_query(qfilter("select_plans"))
async def select_plans(_, query):
  try:
    buttons = InlineKeyboardMarkup([
      [
        InlineKeyboardButton("Free", callback_data="create_project_free"),
        InlineKeyboardButton("Basic", callback_data="create_project_basic")
      ],
      [
        InlineKeyboardButton("Advanced", callback_data="create_project_advance"),
        InlineKeyboardButton("Professional", callback_data="create_project_pro")
      ]
    ])
    await query.message.edit_text(
      "📝 **Choose a plan to create your project:**",
      reply_markup=buttons
    )
  except Exception as e:
    logging.error(f"Error in select_plans callback: {traceback.format_exc()}")
    await query.answer("🚨 An error occurred. Please try again later.", show_alert=True)
