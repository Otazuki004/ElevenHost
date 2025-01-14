from .user_info import UserInfo
from .get_repos import GetRepos
from .delete_user import DeleteUser
from .disconnect_git import DisconnectGit
class Methods(
  UserInfo,
  GetRepos,
  DeleteUser,
  DisconnectGit,
):
  pass
