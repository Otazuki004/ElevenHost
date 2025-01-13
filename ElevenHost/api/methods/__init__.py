from .user_info import UserInfo
from .get_repos import GetRepos
from .delete_user import DeleteUser

class Methods(
  UserInfo,
  GetRepos,
  DeleteUser,
):
  pass
