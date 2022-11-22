from src.data.find_user import FindUser
from src.infra.repo import UserRepository
from src.presenters.interface import RouteInterface
from src.presenters.controllers import FindUserController


def find_user_composer() -> RouteInterface:

    user_repo = UserRepository()
    find_user_usecase = FindUser(user_repository=user_repo)
    find_user_router = FindUserController(find_user_use_case=find_user_usecase)

    return find_user_router
