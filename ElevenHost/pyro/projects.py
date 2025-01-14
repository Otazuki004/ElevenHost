from ElevenHost import app
from pyrogram import filters
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton, Message
from .. import api
from ..others import ask, qfilter
import logging
import asyncio
import traceback 

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
        logging.error(f"Error in select_plans callback: {e}")
        await query.answer("🚨 An error occurred. Please try again later.", show_alert=True)


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


@app.on_callback_query(filters.regex("^deploy_"))
async def fetch_project_logs(_, callback_query):
    try:
        user_id = callback_query.from_user.id
        project_id = int(callback_query.data.split("_")[1])
        project_details = await api.project_info(user_id, project_id)

        if not project_details:
            return await callback_query.answer("⚠️ Unable to fetch project details. Try again later.", show_alert=True)

        if project_details.get("repo") == "Not set":
            repos = await api.get_repos(user_id)
            if not repos:
                return await callback_query.answer("⚠️ No connected repositories found.", show_alert=True)

            buttons = [
                [InlineKeyboardButton(repo.get("name"), callback_data=f"repo_{project_id}_{repo.get('id')}")]
                for repo in repos
            ]

            return await callback_query.message.edit_text(
                "🔄 **Select a repository to connect:**",
                reply_markup=InlineKeyboardMarkup(buttons)
            )

        project_name = project_details.get("name", "Unknown")
        github = project_details.get("repo_name", "Not linked.")
        build_status = project_details.get("status", "Off")
        logs = project_details.get("logs", "No logs available.")
        plan = project_details.get("plan", "Free")
        ram = project_details.get("ram", "None")
        rom = project_details.get("rom", "None")

        status_icon = "🟢 Alive" if build_status.lower().startswith("alive") else "🔴 Offline"
        reply_markup = InlineKeyboardMarkup([
            [InlineKeyboardButton("⛔ Stop", callback_data=f"stop_{project_id}"),
             InlineKeyboardButton("♻️ Redeploy", callback_data=f"redeploy_{project_id}")],
            [InlineKeyboardButton("🔄 Change Repo", callback_data=f"change_repo_{project_id}"),
             InlineKeyboardButton("🔃 Refresh", callback_data=f"refresh_{project_id}")]
        ])

        await callback_query.message.edit_text(
            f"✨ **Eleven Server**\n\n"
            f"📂 **Project Info:**\n"
            f"🔹 **Name:** {project_name}\n"
            f"🔹 **ID:** {project_id}\n"
            f"🔹 **Plan:** {plan}\n\n"
            f"⚙️ **Build Info:**\n"
            f"🔹 **Status:** {status_icon}\n"
            f"🔹 **RAM:** {ram}\n"
            f"🔹 **ROM:** {rom}\n"
            f"🔹 **Repo:** {github}\n\n"
            f"📜 **Logs:**\n"
            f"<pre>{logs}</pre>",
            reply_markup=reply_markup
        )
    except Exception as e:
        logging.error(f"Error in fetch_project_logs callback: {traceback.format_exc()}")
        await callback_query.answer("🚨 An error occurred. Please try again later.", show_alert=True)

@app.on_callback_query(filters.regex("^repo_"))
async def connect_repo(_, callback_query):
    try:
        user_id = callback_query.from_user.id
        data = callback_query.data.split("_")
        project_id = int(data[1])
        repo_id = int(data[2])

        success = await api.set_repo(user_id, project_id, repo_id)
        if success:
            await callback_query.message.edit_text("✅ Repository connected successfully!")
            await fetch_project_logs(_, callback_query)
        else:
            await callback_query.answer("❌ Failed to connect the repository. Try again.", show_alert=True)
    except Exception as e:
        logging.error(f"Error in connect_repo callback: {e}")
        await callback_query.answer("🚨 An error occurred. Please try again later.", show_alert=True)
        

@app.on_callback_query(filters.regex("^stop_"))
async def stop_project(_, callback_query):
    try:
        project_id = int(callback_query.data.split("_")[1])
        await asyncio.sleep(2)
        await callback_query.message.edit_text(
            "🔴 **Project successfully stopped!**",
            reply_markup=InlineKeyboardMarkup([
                [InlineKeyboardButton("🔄 Start Again", callback_data=f"start_{project_id}")]
            ])
        )
    except Exception as e:
        logging.error(f"Error in stop_project callback: {e}")
        await callback_query.answer("🚨 An error occurred. Please try again later.", show_alert=True)


@app.on_callback_query(filters.regex("^start_"))
async def start_project(_, callback_query):
    try:
        project_id = int(callback_query.data.split("_")[1])
        await asyncio.sleep(2)
        await callback_query.message.edit_text("🟢 **Project successfully started!**")
    except Exception as e:
        logging.error(f"Error in start_project callback: {e}")
        await callback_query.answer("🚨 An error occurred. Please try again later.", show_alert=True)


@app.on_callback_query(filters.regex("^redeploy_"))
async def redeploy_project(_, callback_query):
    try:
        project_id = int(callback_query.data.split("_")[1])
        await asyncio.sleep(2)
        await callback_query.message.edit_text("🟢 **Project redeployed successfully!**")
    except Exception as e:
        logging.error(f"Error in redeploy_project callback: {e}")
        await callback_query.answer("🚨 An error occurred. Please try again later.", show_alert=True)


@app.on_callback_query(filters.regex("^refresh_"))
async def refresh_project(_, callback_query):
    try:
        await fetch_project_logs(_, callback_query)
    except Exception as e:
        logging.error(f"Error in refresh_project callback: {e}")
        await callback_query.answer("🚨 An error occurred. Please try again later.", show_alert=True)

@app.on_callback_query(filters.regex("^change_repo_"))
async def change_repo(_, callback_query):
    try:
        user_id = callback_query.from_user.id
        project_id = int(callback_query.data.split("_")[2])
        
        repos = await api.get_repos(user_id)
        if not repos:
            return await callback_query.answer("⚠️ No repositories found.", show_alert=True)

        buttons = [
            [InlineKeyboardButton(repo.get("name"), callback_data=f"select_repo_{project_id}_{repo.get('id')}")]
            for repo in repos
        ]
        buttons.append([InlineKeyboardButton("❌ Cancel", callback_data=f"cancel_change_repo_{project_id}")])

        await callback_query.message.edit_text(
            "🔄 **Select a repository to change and connect to the project:**",
            reply_markup=InlineKeyboardMarkup(buttons)
        )
    except Exception as e:
        logging.error(f"Error in change_repo callback: {e}")
        await callback_query.answer("🚨 An error occurred. Please try again later.", show_alert=True)


@app.on_callback_query(filters.regex("^select_repo_"))
async def select_repo(_, callback_query):
    try:
        user_id = callback_query.from_user.id
        data = callback_query.data.split("_")
        project_id = int(data[2])
        repo_id = int(data[3])

        success = await api.set_repo(user_id, project_id, repo_id)
        if success:
            await callback_query.message.edit_text("✅ Repository connected successfully!")
            await fetch_project_logs(_, callback_query)
        else:
            await callback_query.answer("❌ Failed to connect the repository. Try again.", show_alert=True)
    except Exception as e:
        logging.error(f"Error in select_repo callback: {e}")
        await callback_query.answer("🚨 An error occurred. Please try again later.", show_alert=True)
        
@app.on_callback_query(filters.regex("^cancel_change_repo_"))
async def cancel_change_repo(_, callback_query):
    try:
        project_id = int(callback_query.data.split("_")[2])
        await fetch_project_logs(_, callback_query)
    except Exception as e:
        logging.error(f"Error in cancel_change_repo callback: {e}")
        await callback_query.answer("🚨 An error occurred. Please try again later.", show_alert=True)
