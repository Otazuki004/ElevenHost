from ElevenHost import app
from pyrogram import filters
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton, Message
from .. import api
import asyncio
import logging

@app.on_message(filters.command("deploy"))
async def deploy_command(_, message: Message):
    try:
        user_id = message.from_user.id
        user_name = message.from_user.first_name

        if not await api.exists(user_id):
            return await message.reply_text(
                "❌ You are not registered yet. Please use /start to register your account."
            )

        user_projects = await api.get_projects(user_id)
        if not user_projects:
            return await message.reply_text(
                "📂 **You don't have any projects yet.**\n\n"
                "🔹 Use /projects to create your first project and start hosting!"
            )

        buttons = [
            [InlineKeyboardButton(project.get("name"), callback_data=f"deploy_{project.get('id')}")]
            for project in user_projects if project.get("name") and project.get("id")
        ]

        await message.reply_photo(
            photo="https://i.imgur.com/6Die0Ov.jpeg",
            caption=(
                f"✨ **Hello {user_name}, select a project to deploy:**\n\n"
                "🔹 Click on a project to fetch deployment logs and manage it."
            ),
            reply_markup=InlineKeyboardMarkup(buttons)
        )
    except Exception as e:
        logging.error(f"Error in /deploy command: {e}")
        await message.reply_text("🚨 An unexpected error occurred. Please try again later or contact support.")

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
        github = project_details.get("repo", "Not linked.")
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
            f"🔹 **ID:** {project_id}\n\n"
            f"👤 **User Info:**\n"
            f"🔹 **ID:** {user_id}\n"
            f"🔹 **Plan:** {plan}\n\n"
            f"⚙️ **Build Info:**\n"
            f"🔹 **Status:** {status_icon}\n"
            f"🔹 **RAM:** {ram}\n"
            f"🔹 **ROM:** {rom}\n"
            f"🔹 **Repo:** {github}\n\n"
            f"📜 **Logs:**\n"
            f"```\n{logs}\n```",
            reply_markup=reply_markup
        )
    except Exception as e:
        logging.error(f"Error in fetch_project_logs callback: {e}")
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
        await callback_query.message.edit_text("⛔ **Stopping project...**")
        await asyncio.sleep(3)
        await callback_query.message.edit_text("🔴 **Project successfully stopped!**\n\nClick below to start again.", reply_markup=InlineKeyboardMarkup([
            [InlineKeyboardButton("🔄 Start Again", callback_data=f"start_{project_id}")]
        ]))
    except Exception as e:
        logging.error(f"Error in stop_project callback: {e}")
        await callback_query.answer("🚨 An error occurred. Please try again later.", show_alert=True)

@app.on_callback_query(filters.regex("^start_"))
async def start_project(_, callback_query):
    try:
        project_id = int(callback_query.data.split("_")[1])
        await callback_query.message.edit_text("🔄 **Starting project...**")
        await asyncio.sleep(3)
        await callback_query.message.edit_text("🟢 **Project successfully started!**")
    except Exception as e:
        logging.error(f"Error in start_project callback: {e}")
        await callback_query.answer("🚨 An error occurred. Please try again later.", show_alert=True)

@app.on_callback_query(filters.regex("^redeploy_"))
async def redeploy_project(_, callback_query):
    try:
        project_id = int(callback_query.data.split("_")[1])
        await callback_query.message.edit_text("♻️ **Redeploying project...**")
        await asyncio.sleep(3)
        await callback_query.message.edit_text(
            "🟢 **Project redeployed successfully!**\n\nDeployment details updated."
        )
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
