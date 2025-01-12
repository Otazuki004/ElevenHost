from pyrogram import filters
from pyrogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from ElevenHost import app
from .. import api

@app.on_message(filters.command("upgrade"))
async def upgrade_command(client, message):
    keyboard = InlineKeyboardMarkup([
        [
            InlineKeyboardButton("💼 **Basic Plan**", callback_data="basic_plan"),
            InlineKeyboardButton("🚀 **Advanced Plan**", callback_data="advanced_plan"),
            InlineKeyboardButton("🌟 **Professional Plan**", callback_data="professional_plan")
        ]
    ])

    upgrade_message = """
🔧 **Ready to Level Up Your Eleven Host Plan?**

Choose the perfect plan below and unlock **more projects, more power, and endless possibilities**:

✨ **1️⃣ Basic Plan** – 3 Projects
💸 **₹49 = 100 Coins**

✨ **2️⃣ Advanced Plan** – 5 Projects
💸 **₹99 = 200 Coins**

✨ **3️⃣ Professional Plan** – 7 Projects
💸 **₹199 = 400 Coins**

💥 **Upgrade Today to Supercharge Your Hosting Experience!**
"""
    await message.reply_text(upgrade_message, reply_markup=keyboard)

@app.on_callback_query(filters.regex("basic_plan|advanced_plan|professional_plan"))
async def show_plan_details(client, callback_query):
    plan = callback_query.data.split('_')[0].capitalize()
    
    plan_details = {
        "Basic": "💼 **Basic Plan**\n\n🔹 **3 Projects**\n🔹 **Affordable**: ₹49 (100 Coins)\n🔹 **Get Started** with a solid foundation!",
        "Advanced": "🚀 **Advanced Plan**\n\n🔹 **5 Projects**\n🔹 **Expand Your Reach**: ₹99 (200 Coins)\n🔹 **Ideal** for serious creators.",
        "Professional": "🌟 **Professional Plan**\n\n🔹 **7 Projects**\n🔹 **Unleash Your Potential**: ₹199 (400 Coins)\n🔹 **Go Pro** and scale up your projects!"
    }

    details_message = plan_details.get(plan, "This plan is out of this world!")

    upgrade_buttons = InlineKeyboardMarkup([
        [
            InlineKeyboardButton(f"🚀 Upgrade to {plan} Plan", callback_data=f"upgrade_{plan.lower()}")
        ]
    ])
    
    await callback_query.message.edit_text(details_message, reply_markup=upgrade_buttons)

@app.on_callback_query(filters.regex("upgrade_basic|upgrade_advanced|upgrade_professional"))
async def upgrade_plan(client, callback_query):
    plan = callback_query.data.split('_')[1].capitalize()

    user_id = callback_query.from_user.id
    user_info = await api.user_info(user_id)
    coins = user_info.get('coins', 0)

    plan_requirements = {
        "Basic": {"coins_required": 100, "plan_name": "Basic Plan", "cost": 49},
        "Advanced": {"coins_required": 200, "plan_name": "Advanced Plan", "cost": 99},
        "Professional": {"coins_required": 400, "plan_name": "Professional Plan", "cost": 199}
    }

    required_coins = plan_requirements[plan]["coins_required"]

    if coins >= required_coins:
        await callback_query.message.edit_text(
            f"🎉 **Success!**\n\n🚀 You've officially upgraded to the **{plan} Plan**! Your journey to the next level begins now! 💥"
        )
    else:
        await callback_query.message.edit_text(
            f"⚠️ **Oops!** Not enough coins.\n\nYou need **{required_coins - coins} more coins** to upgrade to the **{plan} Plan**. 🛒"
            "\n\n👉 **Get more coins now** by visiting /shop and unlock your potential!"
  )
