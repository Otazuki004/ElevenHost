import logging
import os
import time
from pyrogram import filters, Client
from motor.motor_asyncio import AsyncIOMotorClient as MongoClient
from variables import MONGODB_URL
from ElevenHost import app

# MongoDB setup
MONGO = MongoClient(MONGODB_URL)
DATABASE = MONGO.ElevenHost

# Logging setup
FORMAT = "[ElevenHost]: %(message)s"
logging.basicConfig(level=logging.INFO, handlers=[logging.FileHandler('logs.txt'),
                                                  logging.StreamHandler()], format=FORMAT)

# Start time
StartTime = time.time()

# Command prefixes
prefix = [".", "!", "?", "*", "$", "#", "/"]

# Function to get readable time
def get_readable_time(seconds: int) -> str:
    count = 0
    ping_time = ""
    time_list = []
    time_suffix_list = ["s", "m", "h", "days"]
    while count < 4:
        count += 1
        remainder, result = divmod(seconds, 60) if count < 3 else divmod(seconds, 24)
        if seconds == 0 and remainder == 0:
            break
        time_list.append(int(result))
        seconds = int(remainder)
    for x in range(len(time_list)):
        time_list[x] = str(time_list[x]) + time_suffix_list[x]
    if len(time_list) == 4:
        ping_time += time_list.pop() + ", "
    time_list.reverse()
    ping_time += ":".join(time_list)
    return ping_time

# Command handler
@app.on_message(filters.command("ping", prefixes=prefix))
async def ping(_, message):
    start_time = time.time()
    await message.reply_text("`Pinging...`")
    end_time = time.time()
    ping_time = round((end_time - start_time) * 1000, 3)
    uptime = get_readable_time(int(time.time() - StartTime))
    await message.reply_text("**I'm Alive !**\n⋙ 🔔 **Ping**: {ping_time}\n⋙ ⬆️ **Uptime**: {uptime}")
