from pyrogram import *
from ElevenHost import *
from pyrogram.type import *
from ElevenHost.others import *
import logging
import traceback 
import asyncio

@app.on_callback_query(filters.regex("^create_project_"))
async def create_project(_, callback_query):
  try:
    data = callback_query.data
    user_id = callback_query.from_user.id
    user_name = callback_query.from_user.first_name
    plan = data.replace('create_project_', '')

    await callback_query.message.edit_text(
      f"🔨 **Hey {user_name}, please provide a name for your new project.**",
      reply_markup=InlineKeyboardMarkup([[
        InlineKeyboardButton("❌ Cancel", callback_data="cancel_create_project")
      ]])
    )

    name = await ask(user=user_id, chat=callback_query.message.chat.id)
    response = await api.create_project(name, user_id, plan)
    if response is True:
      await callback_query.message.reply("✅ Project created successfully!")
    elif response:
      await callback_query.message.reply(response)
    else:
      await callback_query.message.reply("🚨 An error occurred. Please try again later.")
  except Exception as e:
    logging.error(f"Error in create_project callback: {e}")
    await callback_query.answer("🚨 An error occurred. Please try again later.", show_alert=True)
