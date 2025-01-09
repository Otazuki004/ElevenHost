from ElevenHost import app
from pyrogram import filters, Client
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from .. import *
from .. import api

@app.on_message(filters.command(["project", "projects"]))
async def projects(_, message):
  if not await api.exists(message.from_user.id):
    return await message.reply("You didn't register. Please use /start to register!")
  projects = await api.get_projects(message.from_user.id)
  if projects:
    buttons = []
    for x in projects:
      name = x.get('name')
      if name:
        buttons.append([InlineKeyboardButton(name, callback_data="user_project")])
    reply_markup = InlineKeyboardMarkup(buttons)
    await message.reply_photo(
      photo="http://ibb.co/cYwL2ZY",
      caption="Please click your project name",
      reply_markup=reply_markup
    )
  else:
    await message.reply("You don't have any projects yet.")
