from typing import Any
from uuid import UUID
import logging
import requests

from datetime import datetime, timedelta
from utils.errors import ApiException
from services.cruds.group_crud import leave_group
from fastapi import APIRouter, Body, Depends, HTTPException,status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session

from schemas.user import User,UserInDBBase
from schemas.group import GroupCreate
from services.cruds.profile_crud import set_profile
from services.cruds.group_crud import set_group,get_all_groups,join_group,get_selected_group
from services.authenticates.get_current_user import get_current_active_user
from services.logs.set_logs import set_logger
from db import get_db

router = APIRouter()

#ログファイルを作成
#ログファイルを作成
_logger = logging.getLogger(__name__)
set_logger(_logger)

@router.post("/create_groups")
async def create_group(group:GroupCreate,db:Session = Depends(get_db),current_user: User = Depends(get_current_active_user)):
    """
    グループを作成する
    """
    _logger.info("Create group by {current_user.id}")
    try:
        # グループ作成し、作成したグループのidを返す
        group_id = set_group(group,current_user,db)
        if not group_id:
            raise ApiException(
                status_code=status.HTTP_400_BAD_REQUEST,
                status="fail",
                detail="group create error",
            )
        
        #postしたユーザーのこのグループのプロフィールを作成する
        profile_id = set_profile(current_user, group_id, db)
        if not profile_id:
            raise ApiException(
                status_code=status.HTTP_400_BAD_REQUEST,
                status="fail",
                detail="profile create error",
            )
        return group_id
        
    except ApiException as e:
        db.rollback()
        _logger.warning(f"request failed. status_code = {e.status_code} detail = {e.detail}")
        raise e

    except Exception as e:
        _logger.error(f"request failed. Error = {e}")
        db.rollback()
        raise ApiException(
                status_code=status.HTTP_400_BAD_REQUEST,
                status="fail",
                detail="BadRequest",
            )
    

@router.put("/join_group")
def put_join_group(group_id:UUID,password:str,db:Session = Depends(get_db),current_user: User = Depends(get_current_active_user)):
    """
    グループに参加する
    """
    try:
        res = join_group(group_id,password,current_user.id,db)
        return res
    except ApiException as e:
        db.rollback()
        _logger.warning(f"request failed. status_code = {e.status_code} detail = {e.detail}")
        raise e

    except Exception as e:
        _logger.error(f"request failed. Error = {e}")
        db.rollback()
        raise ApiException(
                status_code=status.HTTP_400_BAD_REQUEST,
                status="fail",
                detail="BadRequest",
            )

@router.put("/leave_group")
def put_leave_group(group_id:UUID,db:Session = Depends(get_db),current_user: User = Depends(get_current_active_user)):
    """
    グループから離脱する
    """
    try:
        res = leave_group(group_id,current_user.id,db)
        return res
    except ApiException as e:
        db.rollback()
        _logger.warning(f"request failed. status_code = {e.status_code} detail = {e.detail}")
        raise e

    except Exception as e:
        _logger.error(f"request failed. Error = {e}")
        db.rollback()
        raise ApiException(
                status_code=status.HTTP_400_BAD_REQUEST,
                status="fail",
                detail="BadRequest",
            )

@router.get("/all_groups")
def read_groups(db:Session = Depends(get_db)) -> Any:
    """
    現在登録されているユーザー一覧を取得。
    """
    try:
        groups = get_all_groups(db)
        return groups
    except ApiException as e:
        db.rollback()
        _logger.warning(f"request failed. status_code = {e.status_code} detail = {e.detail}")
        raise e

    except Exception as e:
        _logger.error(f"request failed. Error = {e}")
        db.rollback()
        raise ApiException(
                status_code=status.HTTP_400_BAD_REQUEST,
                status="fail",
                detail="BadRequest",
            )

@router.get("/get_selected_group")
def get_group(group_id:str ,db:Session = Depends(get_db)):
    try:
        group = get_selected_group(group_id,db)
        return group
    except ApiException as e:
        db.rollback()
        _logger.warning(f"request failed. status_code = {e.status_code} detail = {e.detail}")
        raise e

    except Exception as e:
        _logger.error(f"request failed. Error = {e}")
        db.rollback()
        raise ApiException(
                status_code=status.HTTP_400_BAD_REQUEST,
                status="fail",
                detail="BadRequest",
            )
