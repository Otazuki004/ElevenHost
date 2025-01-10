from ElevenHost import app
from pyrogram import filters
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton, Message
from .. import api

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
                [InlineKeyboardButton(project["name"], callback_data=f"project_{project['id']}")]
                for project in user_projects if project.get("name") and project.get("id")
            ]
            buttons.append([InlineKeyboardButton("➕ Create New Project", callback_data="create_project")])

            reply_markup = InlineKeyboardMarkup(buttons)
            await message.reply_photo(
                photo="https://i.ibb.co/cYwL2ZY/placeholder-image.jpg",
                caption=(
                    f"📂 **Hello {user_name}, here are your projects:**\n\n"
                    "🔹 Click on a project to view more details or manage it.\n"
                    "🔹 Create a new project to start something fresh!"
                ),
                reply_markup=reply_markup
            )
        else:
            await message.reply_photo(
                photo="https://i.ibb.co/cYwL2ZY/placeholder-image.jpg",
                caption=(
                    f"📂 **Hello {user_name}, you currently have no projects.**\n\n"
                    "🔹 Use the button below to create your first project and start hosting!\n"
                ),
                reply_markup=InlineKeyboardMarkup([
                    [InlineKeyboardButton("➕ Create New Project", callback_data="create_project")]
                ])
            )
    except Exception as e:
        await message.reply_text(
            "🚨 An unexpected error occurred. Please try again later or contact support.",
            quote=True
        )
        print(f"Error in /projects: {e}")

@app.on_callback_query(filters.regex("^project_"))
async def view_project(_, callback_query):
    try:
        project_id = callback_query.data.split("_")[1]
        project_details = await api.get_project_details(project_id)

        if project_details:
            project_name = project_details.get("name", "Unnamed Project")
            created_at = project_details.get("created_at", "Unknown Date")
            status = project_details.get("status", "Unknown Status")

            details = (
                f"📋 **Project Name:** {project_name}\n"
                f"📅 **Created On:** {created_at}\n"
                f"📊 **Status:** {status}\n\n"
                "Use the buttons below to manage this project."
            )

            reply_markup = InlineKeyboardMarkup([
                [InlineKeyboardButton("🔄 Restart", callback_data=f"restart_{project_id}"),
                 InlineKeyboardButton("❌ Delete", callback_data=f"delete_{project_id}")],
                [InlineKeyboardButton("⬅️ Back to Projects", callback_data="projects_list")]
            ])
            await callback_query.message.edit_text(details, reply_markup=reply_markup)
        else:
            await callback_query.answer("⚠️ Unable to fetch project details. Try again later.", show_alert=True)
    except Exception as e:
        await callback_query.answer("🚨 An error occurred. Please try again later.", show_alert=True)
        print(f"Error in view_project: {e}")

@app.on_callback_query(filters.regex("^create_project$"))
async def create_project(_, callback_query):
    try:
        user_id = callback_query.from_user.id
        user_name = callback_query.from_user.first_name

        await callback_query.message.edit_text(
            f"🔨 **Hey {user_name}, please provide a name for your new project.**",
            reply_markup=InlineKeyboardMarkup([[
                InlineKeyboardButton("Cancel", callback_data="cancel_create_project")
            ]])
        )

        @app.on_message(filters.text)
        async def handle_project_name(msg: Message):
            if msg.from_user.id == user_id:
                project_name = msg.text
                success = await api.create_project(project_name, user_id)

                if success:
                    await msg.reply_text(
                        f"✅ **Project '{project_name}' created successfully!**\n"
                        "You can now manage it in the project list.",
                        quote=True
                    )
                    await projects(_, callback_query.message)
                else:
                    await msg.reply_text("❌ Failed to create project. Try again later.", quote=True)

                app.remove_handler(handle_project_name)
    except Exception as e:
        print(f"Error in create_project callback: {e}")


@app.on_callback_query(filters.regex("^projects_list$"))
async def projects_list(_, callback_query):
    try:
        user_id = callback_query.from_user.id
        user_projects = await api.get_projects(user_id)

        if user_projects:
            buttons = [
                [InlineKeyboardButton(project.get("name"), callback_data=f"project_{project.get('id')}")]
                for project in user_projects if project.get("name") and project.get("id")
            ]
            buttons.append([InlineKeyboardButton("➕ Create New Project", callback_data="create_project")])

            reply_markup = InlineKeyboardMarkup(buttons)
            await callback_query.message.edit_text(
                "📂 **Here are your projects:**\n\n"
                "🔹 Click on a project to view more details or manage it.\n"
                "🔹 Create a new project to start something fresh!",
                reply_markup=reply_markup
            )
        else:
            await callback_query.message.edit_text(
                "📂 **You currently have no projects.**\n\n"
                "🔹 Use the button below to create your first project and start hosting!",
                reply_markup=InlineKeyboardMarkup([
                    [InlineKeyboardButton("➕ Create New Project", callback_data="create_project")]
                ])
            )
    except Exception as e:
        await callback_query.answer("🚨 An error occurred. Please try again later.", show_alert=True)
        print(f"Error in projects_list: {e}")


@app.on_callback_query(filters.regex("^restart_"))
async def restart_project(_, callback_query):
    try:
        project_id = callback_query.data.split("_")[1]
        success = await api.restart_project(project_id)

        if success:
            await callback_query.answer("✅ Project restarted successfully.", show_alert=True)
        else:
            await callback_query.answer("❌ Failed to restart the project. Try again later.", show_alert=True)
    except Exception as e:
        await callback_query.answer("🚨 An error occurred. Please try again later.", show_alert=True)
        print(f"Error in restart_project: {e}")


@app.on_callback_query(filters.regex("^delete_"))
async def delete_project(_, callback_query):
    try:
        project_id = callback_query.data.split("_")[1]
        success = await api.delete_project(project_id)

        if success:
            await callback_query.answer("✅ Project deleted successfully.", show_alert=True)
            await projects_list(_, callback_query)
        else:
            await callback_query.answer("❌ Failed to delete the project. Try again later.", show_alert=True)
    except Exception as e:
        await callback_query.answer("🚨 An error occurred. Please try again later.", show_alert=True)
        print(f"Error in delete_project: {e}")
