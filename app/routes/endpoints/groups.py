from typing import Any
from uuid import UUID
import yaml
import logging
import requests

from datetime import datetime, timedelta
from services.cruds.group_crud import leave_group
from fastapi import APIRouter, Body, Depends, HTTPException,status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session

from schemas.user import User,UserInDBBase
from schemas.group import GroupCreate
from services.cruds.profile_crud import set_profile
from services.cruds.group_crud import set_group,get_all_groups,join_group
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
    # グループ作成し、作成したグループのidを返す
    group_id = set_group(group,current_user,db)
    if not group_id:
        raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Cloud not create group",
                headers={"WWW-Authenticate": "Bearer"},
        )
    
    #postしたユーザーのこのグループのプロフィールを作成する
    profile_id = set_profile(current_user, group_id, db)
    if not profile_id:
        raise  HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Cloud not create user profile",
                headers={"WWW-Authenticate": "Bearer"},
            )
    return group_id
    

@router.put("/join_group")
def put_join_group(group_id:UUID,password:str,db:Session = Depends(get_db),current_user: User = Depends(get_current_active_user)):
    """
    グループに参加する
    """
    res = join_group(group_id,password,current_user.id,db)
    return res

@router.put("/leave_group")
def put_leave_group(group_id:UUID,db:Session = Depends(get_db),current_user: User = Depends(get_current_active_user)):
    """
    グループから離脱する
    """
    res = leave_group(group_id,current_user.id,db)
    return res

@router.get("/all_groups")
def read_groups(db:Session = Depends(get_db)) -> Any:
    """
    現在登録されているユーザー一覧を取得。
    """
    groups = get_all_groups(db)
    return groups

