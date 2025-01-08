# -_- @Otazuki & @KoraxD & @YoursSage
# @Hyper_Speed0™ | @ParadopiaXD

from pyrogram import *
import logging
from variables import *
import os 
from datetime import datetime 
from motor.motor_asyncio import AsyncIOMotorClient
from pymongo import MongoClient
from .api import *
import asyncio

# •••••••••••••••••••••••••••••••••••/\

api = OneApi()

logging.basicConfig( 
  format="[ElevenHost] %(name)s - %(levelname)s - %(message)s",
  handlers=[logging.FileHandler("log.txt"), logging.StreamHandler()],
  level=logging.INFO,
)

MONGO_DB_URI = os.environ.get("MONGO_DB_URI") or VAR_MONGO_DB_URI
MONGO_DB = MongoClient(MONGO_DB_URI) 
DATABASE = AsyncIOMotorClient(MONGO_DB_URI)[f"ElevenHost"]

OneApiUrl = "localhost:8080"
Version = 0.1
bot_start_time = datetime.now()

# -------------------------------------- Main stuffs Ig
API_ID = os.environ.get("API_ID") or VAR_API_ID
API_HASH = os.environ.get("API_HASH") or VAR_API_HASH
HANDLER = [".","~","!","$","#"]
TOKEN = os.environ.get("TOKEN") or VAR_TOKEN
MY_VERSION = 1.2
# _______________________________________
if not API_ID or not API_HASH or not TOKEN or not OneApi:
  raise ValueError("Bro thought he can run anything lol, i mean you forgot some vars put on variables.py")
  exit()
# _-_+_-_+_-_+_-_+_-_+_-_+_-_+_-_+_-_+_-_+_-_+_-_+_-_+_-_+_-_+_-_+_-_+_-_+_-_+_-_+_-_+_-_+_-_+_-_+_-_+_-_+_-_+_-_+_-_+_-_+_-_+_-_+_-_+_|
if len(TOKEN) > 50: app = Client("ElevenHost", session_string=TOKEN, api_id=API_ID, api_hash=API_HASH, plugins=dict(root="ElevenHost/pyro"))
else: app = Client("ElevenHost", bot_token=TOKEN, api_id=API_ID, api_hash=API_HASH, plugins=dict(root="ElevenHost/pyro"))
# ———— R U N ——————————————————————————————————————————————————————————————————————————————————————————————————————————————————————————————————
async def run(command):
  try:
    process = await asyncio.create_subprocess_shell(
      command,
      stdout=asyncio.subprocess.PIPE,
      stderr=asyncio.subprocess.PIPE,
      start_new_session=True
    )
    stdout, stderr = await process.communicate()
    if stdout:
      return stdout.decode().strip()
    if stderr:
      return stderr.decode().strip()
  except Exception as e:
    logging.error(f"Failed to run command '{command}': {e}")
    return False
# _______________________________________________________________    
      
