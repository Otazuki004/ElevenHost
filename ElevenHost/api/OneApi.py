import httpx
import logging
import traceback
import json

log = logging.getLogger("OneApi")

class OneApi:
  def __init__(self):
    self.connected = False
    self.url = None
  
  def connect(self):
    if self.connected: return log.error("You've already connected with OneApi")
    log.info("[^•^] Connecting with OneApi")
    try:
      from .. import OneApiUrl
      self.url = OneApiUrl
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
  
  async def create_user(self, name: str, user_id: int):
    if not self.connected: raise ConnectionError("OneApi isn't connected")
    try:
      data = {"name": name, "user_id": user_id}
      async with httpx.AsyncClient() as mano:
        r = await mano.post(f'{self.url}/create_user/', json=data)
        if r.status_code == 200:
          return True
        elif 'error' in r.json(): log.error(f"[!] OneApi error: {r.json().get('error')}")
    except:
      log.error(traceback.format_exc())
    return False
  
  async def get_projects(self, user_id: int):
    if not self.connected: raise ConnectionError("OneApi isn't connected")
    try:
      data = {"user_id": user_id}
      async with httpx.AsyncClient() as mano:
        r = await mano.post(f'{self.url}/get_projects/', json=data)
        if r.status_code == 200:
          return list(r.json().get('message'))
        elif 'error' in r.json(): log.error(f"[!] OneApi error: {r.json().get('error')}")
    except:
      log.error(traceback.format_exc())
    return False
  
  async def create_project(self, name: str, user_id: int):
    if not self.connected: raise ConnectionError("OneApi isn't connected")
    try:
      data = {"name": name, "user_id": user_id}
      async with httpx.AsyncClient() as mano:
        r = await mano.post(f'{self.url}/create_project/', json=data)
        if r.status_code == 200: return True
        elif 'error' in r.json(): log.error(f"[!] OneApi error: {r.json().get('error')}")
    except: log.error(traceback.format_exc())
    return False
  
  async def delete_project(self, user_id: int, project_id: int):
    if not self.connected: raise ConnectionError("OneApi isn't connected")
    try:
      data = {"user_id": user_id, "project_id": project_id}
      async with httpx.AsyncClient() as mano:
        r = await mano.post(f'{self.url}/delete_project/', json=data)
        if r.status_code == 200: return True
        elif 'error' in r.json(): log.error(f"[!] OneApi error: {r.json().get('error')}")
    except: log.error(traceback.format_exc())
    return False
