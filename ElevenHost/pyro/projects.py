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

@app.on_callback_query(filters.regex("^create_project$"))
async def create_project(_, callback_query):
    try:
        user_id = callback_query.from_user.id
        user_name = callback_query.from_user.first_name
        user_projects = await api.get_projects(user_id)
        user_plan = "Free"
        plan_limits = {"Free": 1, "Basic": 3, "Advanced": 5, "Professional": 7}
        project_limit = plan_limits.get(user_plan, 1)

        if len(user_projects) >= project_limit:
            return await callback_query.answer(
                f"❌ You have reached your project limit for the {user_plan} plan ({project_limit} projects).",
                show_alert=True
            )

        await callback_query.message.edit_text(
            f"🔨 **Hey {user_name}, please provide a name for your new project.**",
            reply_markup=InlineKeyboardMarkup([[
                InlineKeyboardButton("Cancel", callback_data="cancel_create_project")
            ]])
        )
        while True:
            name = await ask(user=user_id, chat=callback_query.message.chat.id)
            creation_status = await api.create_project(name, user_id, user_plan)

            if creation_status is True:
                await callback_query.message.reply("✅ Project created successfully!")
                await callback_query.message.delete()
                break
            elif creation_status:
                await app.send_message(callback_query.message.chat.id, creation_status)
                if 'insufficient' in creation_status.lower():
                    break
            else:
                await app.send_message(callback_query.message.chat.id, "🚨 An error occurred, try again later.")
                break
    except Exception as e:
        logging.error(f"Error in create_project callback: {e}")
        await callback_query.answer("🚨 An error occurred. Please try again later.", show_alert=True)

@app.on_callback_query(filters.regex("^project_"))
async def view_project(_, callback_query):
    try:
        project_id = callback_query.data.split("_")[1]
        project_details = await api.get_project_details(project_id)

        if project_details:
            project_name = project_details.get("name", "Unnamed Project")
            created_at = project_details.get("created_at", "Unknown Date")
            user_id = project_details.get("user_id", "Unknown User")
            github = project_details.get("github", "Not Connected")

            details = (
                f"📋 **Project Name:** {project_name}\n"
                f"🆔 **Project ID:** {project_id}\n"
                f"👤 **User ID:** {user_id}\n"
                f"🌐 **GitHub:** {github}\n\n"
                "🔹 Use the buttons below to manage this project."
            )

            reply_markup = InlineKeyboardMarkup([
                [InlineKeyboardButton("🔄 Reconnect GitHub", callback_data=f"reconnect_{project_id}")],
                [InlineKeyboardButton("❌ Delete", callback_data=f"delete_{project_id}")],
                [InlineKeyboardButton("⬅️ Back to Projects", callback_data="projects_list")]
            ])
            await callback_query.message.edit_text(details, reply_markup=reply_markup)
        else:
            await callback_query.answer("⚠️ Unable to fetch project details. Try again later.", show_alert=True)
    except Exception as e:
        logging.error(f"Error in view_project callback: {e}")
        await callback_query.answer("🚨 An error occurred. Please try again later.", show_alert=True)

@app.on_callback_query(filters.regex("^delete_"))
async def delete_project(_, callback_query):
    try:
        project_id = callback_query.data.split("_")[1]
        project_name = await api.get_project_name(project_id)
        success = await api.delete_project(callback_query.from_user.id, project_id)

        if success:
            await callback_query.answer(f"✅ Project '{project_name}' successfully deleted.", show_alert=True)
            await projects_list(_, callback_query)
        else:
            await callback_query.answer("❌ Failed to delete the project. Try again later.", show_alert=True)
    except Exception as e:
        logging.error(f"Error in delete_project callback: {e}")
        await callback_query.answer("🚨 An error occurred. Please try again later.", show_alert=True)

@app.on_callback_query(filters.regex("^reconnect_"))
async def reconnect_github(_, callback_query):
    try:
        project_id = callback_query.data.split("_")[1]
        github_status = None
    
        if github_status:
            await callback_query.answer("✅ GitHub reconnected successfully.", show_alert=True)
        else:
            await callback_query.answer("❌ Failed to reconnect GitHub. Try again later.", show_alert=True)
    except Exception as e:
        logging.error(f"Error in reconnect_github callback: {e}")
        await callback_query.answer("🚨 An error occurred. Please try again later.", show_alert=True)
