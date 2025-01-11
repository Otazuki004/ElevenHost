import qrcode
from pyrogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from datetime import datetime, timedelta
from ElevenHost import app
from .. import api

plans = {
    'Free': {'price': 0, 'validity': 'Unlimited'},
    'Basic': {'price': 100, 'validity': '30 days'},
    'Advanced': {'price': 500, 'validity': '60 days'},
    'Professional': {'price': 1000, 'validity': '90 days'},
}

def coins_to_currency(coins):
    return coins * 10

def generate_qr(amount, user_id, plan_name):
    upi_link = f"upi://pay?pa=otazuki@jio&pn=Otazuki&am={amount}&cu=INR&tn={user_id}_{plan_name}"
    qr = qrcode.make(upi_link)
    qr.save("upi_qr.png")

@app.on_message(filters.command("myinfo"))
async def myinfo_command(client, message):
    user_id = message.from_user.id
    user_info = await api.user_info(user_id)
    
    coins = user_info.get('coins', 0)
    name = user_info.get('name', 'Unknown')
    projects = user_info.get('projects', 0)
    
    coins_in_inr = coins_to_currency(coins)

    plan_buttons = [
        [InlineKeyboardButton(f"Buy 100 Coins (₹100)", callback_data="buy_100_coins")],
        [InlineKeyboardButton(f"Upgrade to Basic Plan (₹100)", callback_data="upgrade_basic")],
        [InlineKeyboardButton(f"Upgrade to Advanced Plan (₹500)", callback_data="upgrade_advanced")],
        [InlineKeyboardButton(f"Upgrade to Professional Plan (₹1000)", callback_data="upgrade_professional")]
    ]

    reply_markup = InlineKeyboardMarkup(plan_buttons)
    
    user_info_text = f"""
    ✨ ᴜsᴇʀ ɪɴғᴏ
    🔑 **Name:** {name}
    🪙 **Coins:** {coins} (₹{coins_in_inr})
    💼 **Projects:** {projects}

    🔄 Choose an option below to upgrade your plan or buy coins.
    """

    await message.reply_text(user_info_text, reply_markup=reply_markup)

@app.on_callback_query(filters.regex("buy_100_coins"))
async def buy_100_coins(client, callback_query):
    user_id = callback_query.from_user.id
    amount = 100

    generate_qr(amount, user_id, "Coins Purchase")
    
    await callback_query.answer("Click to pay ₹100 for 100 Coins. QR code sent!")
    await callback_query.message.reply_photo("upi_qr.png", caption="Scan the QR Code to proceed with payment. After payment, send the screenshot to Devs.")

@app.on_callback_query(filters.regex("upgrade_basic"))
async def upgrade_basic(client, callback_query):
    user_id = callback_query.from_user.id
    plan_name = "Basic"
    price = plans[plan_name]['price']
    validity = plans[plan_name]['validity']
    
    generate_qr(price, user_id, plan_name)
    
    await callback_query.answer(f"Click to upgrade to {plan_name} Plan (₹{price}). QR code sent!")
    await callback_query.message.reply_photo("upi_qr.png", caption=f"Scan the QR Code to pay ₹{price} and upgrade to the {plan_name} plan. Valid for {validity}. After payment, send the screenshot to Devs.")

@app.on_callback_query(filters.regex("upgrade_advanced"))
async def upgrade_advanced(client, callback_query):
    user_id = callback_query.from_user.id
    plan_name = "Advanced"
    price = plans[plan_name]['price']
    validity = plans[plan_name]['validity']
    
    generate_qr(price, user_id, plan_name)
    
    await callback_query.answer(f"Click to upgrade to {plan_name} Plan (₹{price}). QR code sent!")
    await callback_query.message.reply_photo("upi_qr.png", caption=f"Scan the QR Code to pay ₹{price} and upgrade to the {plan_name} plan. Valid for {validity}. After payment, send the screenshot to Devs.")

@app.on_callback_query(filters.regex("upgrade_professional"))
async def upgrade_professional(client, callback_query):
    user_id = callback_query.from_user.id
    plan_name = "Professional"
    price = plans[plan_name]['price']
    validity = plans[plan_name]['validity']
    
    generate_qr(price, user_id, plan_name)
    
    await callback_query.answer(f"Click to upgrade to {plan_name} Plan (₹{price}). QR code sent!")
    await callback_query.message.reply_photo("upi_qr.png", caption=f"Scan the QR Code to pay ₹{price} and upgrade to the {plan_name} plan. Valid for {validity}. After payment, send the screenshot to Devs.")
