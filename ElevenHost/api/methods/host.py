import httpx
import traceback 

class Host:
  async def host(self, user_id: int, project_id: int):
    if not self.connected: raise ConnectionError("OneApi isn't connected")
    try:
      data = {"user_id": user_id, 'project_id': project_id}
      async with httpx.AsyncClient() as client:
        response = await client.post(f'{self.url}/host/', json=data)
        if response.status_code == 200:
          return response.json().get('message')
    except:
      self.log.error(traceback.format_exc())
    return False
