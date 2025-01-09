import httpx
import logging
import traceback
import json

log = logging.getLogger("OneApi")

class OneApi:
  def __init__(self):
    from .. import OneApiUrl
    self.connected = False
    self.url = OneApiUrl
  def connect(self):
    if self.connected: return log.error("You've already connected with OneApi")
    log.info("[^•^] Connecting with OneApi")
    try:
      self.connected = True
      log.info("OneApi connected!")
    except:
      log.error(traceback.format_exc())
  async def exists(self, user_id: int):
    if not self.connected: raise ConnectionError("OneApi isn't connected")
    try:
      data = {"user_id": user_id}
      async with httpx.AsyncClient() as client:
        response = await client.post(f'{self.url}/exists/', json=data)
        if response.status_code == 200:
          return True
        elif response.status_code == 404:
          return False
        else:
          log.error(f"[!] OneApi error: {response.status_code}: {response.text}")
    except:
      log.error(traceback.format_exc())
    return False
