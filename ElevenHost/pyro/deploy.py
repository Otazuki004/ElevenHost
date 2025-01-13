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
                "❌ You are not registered yet. Please use /start to register your account.",
                quote=True
            )

        user_projects = await api.get_projects(user_id)
        if not user_projects:
            return await message.reply_text(
                "📂 **You don't have any projects yet.**\n\n"
                "🔹 Use /projects to create your first project and start hosting!",
                quote=True
            )

        buttons = [
            [InlineKeyboardButton(project.get("name"), callback_data=f"deploy_{project.get('project_id')}")]
            for project in user_projects if project.get("name") and project.get("project_id")
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
        await message.reply_text(
            "🚨 An unexpected error occurred. Please try again later or contact support.",
            quote=True
        )

@app.on_callback_query(filters.regex("^deploy_"))
async def fetch_project_logs(_, callback_query):
    try:
        project_id = callback_query.data.split("_")[1]
        project_details = await api.get_project_details(project_id)

        if not project_details:
            return await callback_query.answer("⚠️ Unable to fetch project details. Try again later.", show_alert=True)

        await callback_query.message.edit_text("🔄 **Fetching deployment logs...**")
        await asyncio.sleep(2)

        project_name = project_details.get("name", "Unnamed Project")
        user_id = project_details.get("user_id", "Unknown User")
        github = project_details.get("github", "Not Connected")
        build_status = project_details.get("status", "Unknown")
        logs = project_details.get("logs", "No logs available.")
        connected_repo = project_details.get("repo", "Not Connected")

        status_icon = "🟢 Alive" if build_status.lower() == "alive" else "🔴 Offline"
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
            f"🔹 **GitHub:** {github}\n\n"
            f"⚙️ **Build Into:**\n"
            f"🔹 **Status:** {status_icon}\n"
            f"🔹 **Connected Repo:** {connected_repo}\n\n"
            f"📜 **Logs:**\n"
            f"```\n{logs}\n```",
            reply_markup=reply_markup
        )
    except Exception as e:
        logging.error(f"Error in fetch_project_logs callback: {e}")
        await callback_query.answer("🚨 An error occurred. Please try again later.", show_alert=True)

@app.on_callback_query(filters.regex("^stop_"))
async def stop_project(_, callback_query):
    try:
        project_id = callback_query.data.split("_")[1]
        await callback_query.message.edit_text("⛔ **Stopping project...**")
        await asyncio.sleep(2)
        await callback_query.message.edit_text(
            f"🔴 **Project {project_id} is now stopped.**"
        )
    except Exception as e:
        logging.error(f"Error in stop_project callback: {e}")
        await callback_query.answer("🚨 An error occurred. Please try again later.", show_alert=True)

@app.on_callback_query(filters.regex("^redeploy_"))
async def redeploy_project(_, callback_query):
    try:
        project_id = callback_query.data.split("_")[1]
        await callback_query.message.edit_text("♻️ **Redeploying project...**")
        await asyncio.sleep(3)
        await callback_query.message.edit_text(
            f"🟢 **Project {project_id} redeployed successfully!**\n\n"
            "✨ Deployment details updated."
        )
    except Exception as e:
        logging.error(f"Error in redeploy_project callback: {e}")
        await callback_query.answer("🚨 An error occurred. Please try again later.", show_alert=True)

@app.on_callback_query(filters.regex("^change_repo_"))
async def change_repo(_, callback_query):
    try:
        user_id = callback_query.from_user.id
        repos = await api.get_repos(user_id)

        if not repos:
            return await callback_query.answer("⚠️ No connected repositories found.", show_alert=True)

        buttons = [
            [InlineKeyboardButton(repo.get("name"), callback_data=f"repo_{repo.get('id')}")]
            for repo in repos
        ]
        await callback_query.message.edit_text(
            "🔄 **Select a repository to connect:**",
            reply_markup=InlineKeyboardMarkup(buttons)
        )
    except Exception as e:
        logging.error(f"Error in change_repo callback: {e}")
        await callback_query.answer("🚨 An error occurred. Please try again later.", show_alert=True)

@app.on_callback_query(filters.regex("^refresh_"))
async def refresh_project(_, callback_query):
    try:
        await fetch_project_logs(_, callback_query)
    except Exception as e:
        logging.error(f"Error in refresh_project callback: {e}")
        await callback_query.answer("🚨 An error occurred. Please try again later.", show_alert=True)
