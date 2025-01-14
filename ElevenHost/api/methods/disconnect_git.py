import httpx
import traceback

class DisconnectGit:
  async def disconnect_git(self, user_id: int):
    if not self.connected: raise ConnectionError("OneApi isn't connected")
    try:
      data = {"user_id": user_id}
      async with httpx.AsyncClient() as client:
        response = await client.post(f'{self.url}/disconnect_git/', json=data)
        if response.status_code == 200:
          return True
    except:
      self.log.error(traceback.format_exc())
    return False
