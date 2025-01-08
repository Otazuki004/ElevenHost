import asyncio
import websockets
import logging
import traceback
import json

log = logging.getLogger("OneApi")

class OneApi:
  def __init__(self):
    self.ws = None
    exists_ws = None
  async def connect_routes(self):
    from .. import OneApiUrl
    self.exists_ws = await websockets.connect(f"{OneApiUrl}/ws/exists/")
    self.ws = True
  def connect(self):
    if self.ws: log.error("You've already connected with OneApi")
    log.info("[^•^] Connecting with OneApi")
    try:
      loop = asyncio.get_event_loop()
      if loop.is_running(): asyncio.ensure_future(self.connect_routes())
      else: loop.run_until_complete(self.connect_routes())
      log.info("OneApi connected!")
    except: log.info(f"OneApi connection failed: {(traceback.format_exc())}")
  async def exists(self, user_id: int):
    if not self.exists_ws: raise ConnectionError("OneApi is not connected")
    try:
      await self.ws.send(s)
      answer = json.loads(await self.ws.recv())
      if not 'error' in answer: return True
      else:
        log.error(f"[!] OneApi error: {answer}")
    except: log.error((traceback.format_exc()))
    return True
