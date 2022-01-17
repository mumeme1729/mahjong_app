from sys import prefix
from fastapi import APIRouter

from .endpoints import users,groups,login,games

api_router = APIRouter()

api_router.include_router(login.router,tags=['login'])
api_router.include_router(users.router,prefix="/users",tags=['users'])
api_router.include_router(groups.router,prefix="/groups",tags=['groups'])
api_router.include_router(games.router,prefix="/games",tags=['games'])