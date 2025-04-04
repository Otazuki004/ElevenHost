from ElevenHost import app
from .. import api
from pyrogram import filters
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton, Message
from pyrogram.errors import UserAlreadyParticipant
import logging
import asyncio
from pyrogram.enums import ChatType

@app.on_message(filters.command('start'))
async def start(_, message: Message):
  try:
    user_id = message.from_user.id
    user_name = message.from_user.first_name

    if not await api.exists(user_id):
      mano_ily = await api.create_user(user_name, user_id)
      if not mano_ily:
        if message.chat.type != ChatType.PRIVATE:
          return await message.reply("You cannot register in groups, please send /start on private.")
        mano = InlineKeyboardMarkup([[InlineKeyboardButton("Connect git", url=f"https://github.com/apps/ElevenHost/installations/new?state={message.from_user.id}")]])
        return await message.reply("You have to connect with your github account to use this bot.", reply_markup=mano)
      else: asyncio.create_task(app.send_message(-1001859707851, f"**New user registered**\n\n**Name:** {message.from_user.first_name}\n**User Id:** {message.from_user.id}"))
    
    caption_text = (
      "𝗘𝗟𝗘𝗩𝗘𝗡 𝗛𝗢𝗦𝗧\n\n"
      "🍃 We provide the most reliable 🧡 and high-performance 🌩️ hosting solutions with a focus on simplicity and ease of use.\n"
      "Enjoy fast and secure hosting with unlimited potential! 🗝️ (°ᴗ°) 🥀✨\n\n"
      "🦋 Channel: @ElevenHost\n"
      "👾 Support: @ElevenHostSupport\n"
    )

    keyboard = InlineKeyboardMarkup([
      [InlineKeyboardButton("🌟 Get Started", callback_data="get_started")],
      [InlineKeyboardButton("👩‍💻 Contact Support", url="https://t.me/ElevenHostSupport")]
    ])

    await message.reply_photo(
      photo="https://i.imgur.com/rAGtzwy.jpeg",
      caption=caption_text,
      reply_markup=keyboard
    )
  except Exception as e:
    logging.error(f"Error in /start: {e}")
    await message.reply("🚨 An error occurred while processing your request. Please try again later.")

@app.on_callback_query(filters.regex("get_started"))
async def get_started(_, callback_query):
  try:
    await callback_query.answer("Let's get started! 🚀", show_alert=True)
    welcome_text = (
      "✨ Welcome to Eleven Host! ✨\n\n"
      "💻 Reliable and fast hosting solutions are just a click away.\n"
      "🔗 Use the menu below to explore our services and manage your account.\n\n"
      "💡 Need help? Contact Support anytime!"
    )
    keyboard = InlineKeyboardMarkup([
      [InlineKeyboardButton("🌩️ View Hosting Info", callback_data="view_info")],
      [InlineKeyboardButton("👩‍💻 Contact Support", url="https://t.me/ElevenHostSupport")]
    ])
    await callback_query.message.edit_text(welcome_text, reply_markup=keyboard, disable_web_page_preview=True)
  except Exception as e:
    logging.error(f"Error in get_started: {e}")
    await callback_query.answer("An error occurred. Please try again.", show_alert=True)

@app.on_callback_query(filters.regex("view_info"))
async def view_info(_, callback_query):
  try:
    info_text = (
      "✨ Our Hosting Features ✨\n\n"
      "⚡ High-Speed Hosting\n"
      "🔒 Advanced Security\n"
      "🎯 User-Friendly Dashboard\n\n"
      "Contact Support for detailed assistance or to get started!"
    )
    keyboard = InlineKeyboardMarkup([
      [InlineKeyboardButton("⬅️ Back", callback_data="get_started")]
    ])
    await callback_query.message.edit_text(info_text, reply_markup=keyboard, disable_web_page_preview=True)
  except Exception as e:
    logging.error(f"Error in view_info: {e}")
    await callback_query.answer("An error occurred. Please try again.", show_alert=True)
