from pyrogram import *
from ElevenHost import *
from pyrogram.types import *
from ElevenHost.others import *
import logging
import traceback 
import asyncio
import aiofiles

@app.on_callback_query(filters.regex("^deploy_"))
async def view_project(_, callback_query):
  try:
    user_id = callback_query.from_user.id
    project_id = int(callback_query.data.split("_")[1])
    project_details = await api.project_info(user_id, project_id)

    if not project_details:
      return await callback_query.answer("⚠️ Unable to fetch project details. Try again later.", show_alert=True)

    if project_details.get("repo") == 0:
      repos = await api.get_repos(user_id)
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
      [InlineKeyboardButton("🔄 Change Repo", callback_data=f"change_repo_{project_id}_{user_id}"),
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
      f"<pre>{logs[200:]}</pre>",
      reply_markup=reply_markup
    )
    if len(logs) > 200:
      async with aiofiles.open(f'log{user_id}.txt', mode='w') as fk:
        await fk.write(logs)
      await callback_query.message.reply_document(f'log{user_id}.txt')
      await run(f'rm -rf log{user_id}.txt')
  except Exception as e:
    logging.error(f"Error in view_project callback: {traceback.format_exc()}")
    await callback_query.answer("🚨 An error occurred. Please try again later.", show_alert=True)
