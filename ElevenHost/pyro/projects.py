from ElevenHost import app
from pyrogram import filters
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton, Message
from .. import api
import logging

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
        user_plan = "Free"
        plan_limits = {"Free": 1, "Basic": 3, "Advanced": 5, "Professional": 7}
        project_limit = plan_limits.get(user_plan, 1)

        if user_projects:
            buttons = []
            for project in user_projects:
                if project.get('name') and project.get('project_id'):
                    buttons.append(
                        [InlineKeyboardButton(project.get("name"), callback_data=f"project_{project.get('project_id')}")]
                    )

            if len(user_projects) < project_limit:
                buttons.append([InlineKeyboardButton("➕ Create New Project", callback_data="create_project")])

            reply_markup = InlineKeyboardMarkup(buttons)
            await message.reply_photo(
                photo="https://i.imgur.com/6Die0Ov.jpeg",
                caption=(
                    f"📂 **Hello {user_name}, here are your projects:**\n\n"
                    "🔹 Click on a project to view more details or manage it.\n"
                    f"🔹 Plan: {user_plan} | Limit: {len(user_projects)}/{project_limit}"
                ),
                reply_markup=reply_markup
            )
        else:
            await message.reply_photo(
                photo="https://i.imgur.com/6Die0Ov.jpeg",
                caption=(
                    f"📂 **Hello {user_name}, you currently have no projects.**\n\n"
                    "🔹 Use the button below to create your first project and start hosting!\n"
                    f"🔹 Plan: {user_plan} | Limit: 0/{project_limit}"
                ),
                reply_markup=InlineKeyboardMarkup([
                    [InlineKeyboardButton("➕ Create New Project", callback_data="create_project")]
                ])
            )
    except Exception as e:
        logging.error(f"Error in /projects command: {e}")
        await message.reply_text(
            "🚨 An unexpected error occurred. Please try again later or contact support.",
            quote=True
        )

