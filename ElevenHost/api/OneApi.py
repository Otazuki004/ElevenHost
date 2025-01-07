import asyncio
import websockets
from ElevenHost import OneApiUrl
import logging
import traceback
import json

log = logging.getLogger("OneApi")

class OneApi:
  def __init__(self):
    self.ws = None
  def connect(self):
    if self.ws: log.error("You've already connected with OneApi")
    log.info("[^•^] Connecting with OneApi")
    try:
      loop = asyncio.get_event_loop()
      if loop.is_running(): self.ws = asyncio.ensure_future(websockets.connect(f"{OneApiUrl}/ws/ElevenHost/"))
      else: self.ws = loop.run_until_complete(websockets.connect(f"{OneApiUrl}/ws/ElevenHost/"))
      log.info("OneApi connected!")
    except: log.info(f"OneApi connection failed: {traceback.format_exc}")
  async def exists(self, user_id: int):
    if not self.ws: raise ConnectionError("OneApi is not connected")
    try:
      s = {'check_user': user_id}
      await self.ws.send(s)
      answer = json.loads(await self.ws.recv())
      if not 'error' in answer: return answer.get('data')
      else:
        log.error(f"[!] OneApi error: {answer}")
    except: log.error(traceback.format_exc())
    return False
