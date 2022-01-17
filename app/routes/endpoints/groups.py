from typing import Any
from uuid import UUID
import yaml
import logging
import requests

from datetime import datetime, timedelta
from services.cruds.group_crud import join_group
from fastapi import APIRouter, Body, Depends, HTTPException,status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session

from schemas.user import User,UserInDBBase
from schemas.group import GroupCreate
from services.cruds.group_crud import set_group,get_all_groups
from services.authenticates.get_current_user import get_current_active_user
from services.logs.set_logs import set_logger
from db import get_db

router = APIRouter()

with open('settings.yaml', 'r') as yml:
    settings = yaml.safe_load(yml)

#ログファイルを作成
_uvicorn_accsess_logger = set_logger("uvicorn.access",file_name = 'access')
_ormapper_logger = set_logger("sqlalchemy.engine",file_name='ormapper')
_logger = set_logger(__name__)

@router.post("/create_groups")
async def create_group(group:GroupCreate,db:Session = Depends(get_db),current_user: User = Depends(get_current_active_user)):
    """
    グループを作成する
    """
    _logger.info("Create group by {current_user.email}")
    #作成者をグループ作成時に追加する
    user = UserInDBBase(
        id = current_user.id,
        emal = current_user.email,
        is_active = current_user.is_active
    )

    res = set_group(group,user,db)
    return res

@router.put("/join_group")
def put_join_group(group_id:UUID,password:str,db:Session = Depends(get_db),current_user: User = Depends(get_current_active_user)):
    """
    グループに参加する
    """
    res = join_group(group_id,password,current_user.id,db)
    return res


@router.get("/all_groups")
def read_groups(db:Session = Depends(get_db)) -> Any:
    """
    現在登録されているユーザー一覧を取得。
    """
    groups = get_all_groups(db)
    return groups