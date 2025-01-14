import httpx
import traceback

class SetRepo:
  async def set_repo(self, user_id: int, project_id: int, repo_id: int):
    if not self.connected: raise ConnectionError("OneApi isn't connected")
    try:
      data = {"user_id": user_id, "project_id": project_id, 'repo_id': repo_id}
      async with httpx.AsyncClient() as client:
        response = await client.post(f'{self.url}/set_repo/', json=data)
        if response.status_code == 200:
          return True
        self.log.info(f"Set repo 13: {response.text}")
    except:
      self.log.error(traceback.format_exc())
    return False
