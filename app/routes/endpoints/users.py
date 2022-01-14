from typing import Any
import yaml

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from schemas.user import User
from services.cruds.user_crud import get_all_users, get_user_by_id
from services.logs.set_logs import set_logger
from services.authenticates.get_current_user import get_current_active_user
from db import get_db

router = APIRouter()

with open('settings.yaml', 'r') as yml:
    settings = yaml.safe_load(yml)

#ログファイルを作成
_uvicorn_accsess_logger = set_logger("uvicorn.access",file_name = 'access')
_ormapper_logger = set_logger("sqlalchemy.engine",file_name='ormapper')
_logger = set_logger(__name__)


@router.get("/me/", response_model=User)
async def read_users_me(current_user: User = Depends(get_current_active_user)):
    """
    現在ログインしているユーザーを返す。
    """
    _logger.info(f"get current user : {current_user.email}")
    print(f"current_user {current_user.id}")
    return current_user

@router.get("/all_users")
def read_users(db:Session = Depends(get_db)) -> Any:
    """
    現在登録されているユーザー一覧を取得。
    """
    users = get_all_users(db)
    return users

@router.get("/user_id")
def read_users(id:str,db:Session = Depends(get_db)) -> Any:
    """
    現在登録されているユーザー一覧を取得。
    """
    users = get_user_by_id(id,db)
    return users