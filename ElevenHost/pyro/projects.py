from ElevenHost import app
from pyrogram import filters
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton, Message
from .. import api
from ..others import ask, qfilter
import logging
import asyncio


@app.on_message(filters.command(["project", "projects"]))
async def projects(_, message: Message):
    try:
        user_id = message.from_user.id
        user_name = message.from_user.first_name

        if not await api.exists(user_id):
            return await message.reply_text(
                "❌ You are not registered yet. Please use /start to register your account.",
                quote=True
            )

        user_projects = await api.get_projects(user_id)
        if user_projects:
            buttons = [
                [InlineKeyboardButton(project["name"], callback_data=f"deploy_{project['project_id']}")]
                for project in user_projects if project.get("name") and project.get("project_id")
            ]
            buttons.append([InlineKeyboardButton("➕ Create New Project", callback_data="select_plans")])

            reply_markup = InlineKeyboardMarkup(buttons)
            await message.reply_photo(
                photo="https://i.imgur.com/6Die0Ov.jpeg",
                caption=(
                    f"📂 **Hello {user_name}, here are your projects:**\n\n"
                    "🔹 Click on a project to view more details or manage it.\n"
                ),
                reply_markup=reply_markup
            )
        else:
            await message.reply_photo(
                photo="https://i.imgur.com/6Die0Ov.jpeg",
                caption=(
                    f"📂 **Hello {user_name}, you currently have no projects.**\n\n"
                    "🔹 Use the button below to create your first project and start hosting!\n"
                ),
                reply_markup=InlineKeyboardMarkup([
                    [InlineKeyboardButton("➕ Create New Project", callback_data="select_plans")]
                ])
            )
    except Exception as e:
        logging.error(f"Error in /projects command: {e}")
        await message.reply_text(
            "🚨 An unexpected error occurred. Please try again later or contact support.",
            quote=True
        )

