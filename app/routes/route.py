import logging
from sys import prefix
from fastapi import APIRouter
from services.logs.set_logs import set_logger
from .endpoints import users,groups,login,games

_uvicorn_accsess_logger = logging.getLogger("uvicorn.access")
set_logger(_uvicorn_accsess_logger, file_name = 'access')
_ormapper_logger = logging.getLogger("sqlalchemy.engine")
set_logger(_ormapper_logger, file_name = 'ormapper', log_level = 'WARN')


api_router = APIRouter()

api_router.include_router(login.router,tags=['login'])
api_router.include_router(users.router,prefix="/users",tags=['users'])
api_router.include_router(groups.router,prefix="/groups",tags=['groups'])
api_router.include_router(games.router,prefix="/games",tags=['games'])