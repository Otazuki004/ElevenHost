from ElevenHost import *
from pyrogram import *
from pyrogram import idle 
from .api import *
from .pyro.callbacks import *

if __name__ == '__main__':
  api.connect()
  app.start()
  idle()
