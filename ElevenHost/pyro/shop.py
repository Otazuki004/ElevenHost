import os
import qrcode
from pyrogram import filters
from ElevenHost import app
from pyrogram.types import InlineKeyboardButton, InlineKeyboardMarkup

@app.on_message(filters.command("shop"))
async def shop_command(client, message):
    keyboard = InlineKeyboardMarkup([
        [
            InlineKeyboardButton("🪙 100 Coins - ₹49", callback_data="buy_100"),
            InlineKeyboardButton("🪙 200 Coins - ₹99", callback_data="buy_200")
        ]
    ])

    shop_message = """
🛒 **Welcome to the Eleven Host Shop!**  
✨ Here’s your chance to power up with some shiny new coins!

🔹 **100 Coins** - `₹49`
🔹 **200 Coins** - `₹99`

🔑 Simply tap on your choice and make the payment securely. You'll get a QR code to complete the transaction. 🏁
"""

    await message.reply_text(shop_message, reply_markup=keyboard)

@app.on_callback_query(filters.regex("buy_100"))
async def buy_100_coins(client, callback_query):
    upi_link = "upi://pay?pa=otazuki@jio&pn=Otazuki&am=49&cu=INR&tn=" + f"{callback_query.from_user.id}_100coins"
    qr = qrcode.make(upi_link)

    qr_image_path = qr.save()

    await callback_query.message.delete()
    await callback_query.message.reply_photo(
        qr_image_path, 
        caption=f"🖼️ **Scan this QR Code to pay ₹49 for 100 Coins.**\n\n💡 **How to pay:**\n1. Open your UPI app 📱\n2. Scan the QR code 🎯\n3. Confirm payment 🔒\n\nOnce paid, send a screenshot to the Devs for verification. 💬\n\n🔒 **Your coins will be added once verified!**"
    )

@app.on_callback_query(filters.regex("buy_200"))
async def buy_200_coins(client, callback_query):
    upi_link = "upi://pay?pa=otazuki@jio&pn=Otazuki&am=99&cu=INR&tn=" + f"{callback_query.from_user.id}_200coins"
    qr = qrcode.make(upi_link)

    qr_image_path = qr.save()

    await callback_query.message.delete()
    await callback_query.message.reply_photo(
        qr_image_path, 
        caption=f"🖼️ **Scan this QR Code to pay ₹99 for 200 Coins.**\n\n💡 **How to pay:**\n1. Open your UPI app 📱\n2. Scan the QR code 🎯\n3. Confirm payment 🔒\n\nOnce paid, send a screenshot to the Devs for verification. 💬\n\n🔒 **Your coins will be added once verified!**"
    )
