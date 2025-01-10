import httpx
import logging
import traceback
import json
from ..OneApi import *

async def user_info(self, user_id: int):
    if not self.connected: raise ConnectionError("OneApi isn't connected")
    try:
      data = {"user_id": user_id}
      async with httpx.AsyncClient() as client:
        response = await client.post(f'{self.url}/user_info/', json=data)
        if response.status_code == 200:
          return response.json().get('message')
    except:
      log.error(traceback.format_exc())
    return False
