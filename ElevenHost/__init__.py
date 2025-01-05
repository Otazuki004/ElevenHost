# -_- @Otazuki & @KoraxD & @Paradopia
# @Hyper_Speed0™ 

from pyrogram import *
import logging
from variables import *
import os 
from motor import AsyncIOMotorClient
from pymongo import MongoClient
# •••••••••••••••••••••••••••••••••••/\

logging.basicConfig( 
  format="[Sophia-Beta] %(name)s - %(levelname)s - %(message)s",
  handlers=[logging.FileHandler("log.txt"), logging.StreamHandler()],
  level=logging.INFO,
)

MONGO_DB_URI = os.environ.get("MONGO_DB_URI") or VAR_MONGO_DB_URI
MONGO_DB = MongoClient(MONGO_DB_URI) 
DATABASE = AsyncIOMotorClient(MONGO_DB_URI)[f"ElevenHost"]

OneApi = ""
Version = 0.1

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
if len(TOKEN) > 50: Client("ElevenHost", session_string=TOKEN, api_id=API_ID, api_hash=API_HASH, plugins=dict(root="Eleven/modules"))
else: Client("ElevenHost", bot_token=TOKEN, api_id=API_ID, api_hash=API_HASH, plugins=dict(root="Eleven/modules"))
# ——————————————————————————————————————————————————————————————————————————————————————————————————————————————————————————————————————
