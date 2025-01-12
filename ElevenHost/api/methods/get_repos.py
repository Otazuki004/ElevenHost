import httpx
import logging
import traceback

class GetRepos:
  async def get_repos(self, user_id: int):
    if not self.connected: raise ConnectionError("OneApi isn't connected")
    try:
      data = {"user_id": user_id}
      async with httpx.AsyncClient(timeout=30) as client:
        response = await client.post(f'{self.url}/get_repos/', json=data)
        self.log.info(response.text)
        if response.status_code == 200:
          return response.json().get('message')
        elif 'error' in response.text:
          self.log.error(f"[!] OneApi error: {response.status_code}: {response.text}")
    except:
      self.log.error(traceback.format_exc())
    return False
