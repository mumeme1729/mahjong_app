from typing import Any
import yaml


from fastapi import APIRouter, Depends,HTTPException,status
from sqlalchemy.orm import Session

from schemas.game import GameCreate,Game
from schemas.user import User
from services.cruds.user_crud import get_all_users, get_user_by_id
from services.cruds.group_crud import get_group_by_id
from services.cruds.game_crud import set_game
from services.logs.set_logs import set_logger
from services.cruds.profile_crud import get_profile_by_user_and_group
from services.authenticates.get_current_user import get_current_active_user
from db import get_db

router = APIRouter()

with open('settings.yaml', 'r') as yml:
    settings = yaml.safe_load(yml)

#ログファイルを作成
_uvicorn_accsess_logger = set_logger("uvicorn.access",file_name = 'access')
_ormapper_logger = set_logger("sqlalchemy.engine",file_name='ormapper')
_logger = set_logger(__name__)


@router.post("/create_game/", response_model=Game)
async def create_game(game_data:GameCreate,db:Session = Depends(get_db),current_user: User = Depends(get_current_active_user)):
    """
    対局テーブルを作成する
    """
    _logger.info(f"get current user : {current_user.email}")
    # グループのチェック
    group = get_group_by_id(game_data.group_id,db)
    # グループが存在しない場合はBAD_REQUEST
    if not group:
        _logger.warning(f"Group does not exist. : {game_data.group_id}")
        raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Group does not exist.",
        )
    # そのグループにPOSTしたユーザーが属しているか
    # プロフィールを取得
    profile = get_profile_by_user_and_group(current_user.id,group.id,db)
    if profile is not None:
        res = set_game(game_data,db)
        return res        
    _logger.warning(f" this user doesn't belong to this group.")
    raise HTTPException(
        status_code=status.HTTP_400_BAD_REQUEST,
        detail="don't belong to this group",
        headers={"WWW-Authenticate": "Bearer"},
    )
    

