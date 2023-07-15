from typing import Any, Optional, Union
from uuid import UUID
import logging
import requests
from services.cruds.game_crud import get_gams_within_specified_period
from services.cruds.profile_crud import update_profile_rate
from services.cruds.rank_crud import get_all_ranks
from services.cruds.profile_crud import update_profile_by_user_id
from services.cruds.profile_crud import get_profile_by_user_and_group
from services.cruds.group_crud import get_profiles
from services.cruds.game_crud import get_recently_game
import boto3
import config
from datetime import datetime, timedelta
from schemas.response import CommonResponseSuccess
from utils.errors import ApiException
from services.cruds.group_crud import leave_group
from fastapi import APIRouter, Body, Depends, HTTPException,status, UploadFile, File
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session

from schemas.user import User,UserInDBBase
from schemas.group import GroupCreate
from services.cruds.profile_crud import set_profile
from services.cruds.group_crud import set_group,get_all_groups,join_group,get_selected_group, update_group_image
from services.authenticates.get_current_user import get_current_active_user
from services.logs.set_logs import set_logger
from db import get_db

router = APIRouter()

#ログファイルを作成
#ログファイルを作成
_logger = logging.getLogger(__name__)
set_logger(_logger)



@router.post("/create_groups")
async def create_group(group:GroupCreate= Depends(), upload_file: UploadFile = File(None), db:Session = Depends(get_db), current_user: User = Depends(get_current_active_user)):
    """
    グループを作成する
    """
    _logger.info("Create group by {current_user.id}")
    try:
        group_id = set_group(group,current_user,db)
        if not group_id:
            raise ApiException(
                status_code=status.HTTP_400_BAD_REQUEST,
                status="fail",
                detail="group create error",
            )
        # グループに画像を設定する
         #postしたユーザーのこのグループのプロフィールを作成する
        profile_id = set_profile(current_user, group_id, db)
        if not profile_id:
            raise ApiException(
                status_code=status.HTTP_400_BAD_REQUEST,
                status="fail",
                detail="profile create error",
            )
    
        path = None
        if upload_file is not None:
            s3 = boto3.client('s3',
                aws_access_key_id=config.AWS_ACCESS_KEY,
                aws_secret_access_key=config.AWS_SECRET_ACCESS_KEY,
                region_name=config.AWS_REGION
            )

            dt_now = datetime.now()
            dt = dt_now.strftime('%Y%m%d%H%M%S')
            filename = f"{group.title}_{dt}_{upload_file.filename}"
            Bucket = "mahjong-group-image"
            Key = f'group_image/{group_id}/{filename}'
            s3.put_object(Body=upload_file.file, Bucket =Bucket, Key =Key)
            path = f"https://{Bucket}.s3-{config.AWS_REGION}.amazonaws.com/{Key}"
            #画像を設定する
            update_group_image(group_id, path, db)
        return {"status": "ok", "detail": group_id}
        
    except ApiException as e:
        db.rollback()
        _logger.warning(f"request failed. status_code = {e.status_code} detail = {e.detail}")
        raise e

    except Exception as e:
        print(e)
        _logger.error(f"request failed. Error = {e}")
        db.rollback()
        raise ApiException(
                status_code=status.HTTP_400_BAD_REQUEST,
                status="fail",
                detail="BadRequest",
            )
    

@router.put("/join_group", response_model = CommonResponseSuccess)
def put_join_group(group_id:UUID,password:str,db:Session = Depends(get_db),current_user: User = Depends(get_current_active_user)):
    """
    グループに参加する
    """
    try:
        res = join_group(group_id,password,current_user.id,db)
        return {"status":"ok"}
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

@router.put("/leave_group", response_model = CommonResponseSuccess)
def put_leave_group(group_id:UUID,db:Session = Depends(get_db),current_user: User = Depends(get_current_active_user)):
    """
    グループから離脱する
    """
    try:
        res = leave_group(group_id,current_user.id,db)
        return {"status":"ok"}
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

@router.get("/get_selected_group",)
def get_group(group_id:str ,db:Session = Depends(get_db),current_user: User = Depends(get_current_active_user)):
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

@router.get("/get_selected_group_recently_games")
def get_recently_games(group_id:str ,db:Session = Depends(get_db),current_user: User = Depends(get_current_active_user)):
    try:
        recently_games = get_recently_game(group_id,db)
        return recently_games
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

@router.get("/get_games_specified_period")
def get_games_specified_period(group_id:str,date_from:str,date_until:str, db:Session = Depends(get_db),current_user: User = Depends(get_current_active_user)):
    """
    指定された期間の対局記録を取得する
    """
    try:
        games = get_gams_within_specified_period(group_id,date_from,date_until,db)
        return games
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


@router.get("/profiles")
def get_profiles_list(group_id:str, db:Session = Depends(get_db),current_user: User = Depends(get_current_active_user)) -> Any:
    """
    現在グループに属いている全プロフィールを取得
    """
    try:
        groups = get_profiles(group_id,db)
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

@router.get("/is_joind")
def get_is_joind( db:Session = Depends(get_db),current_user: User = Depends(get_current_active_user)) -> Any:
    """
    グループに参加しているかどうか確認を行う
    """
    try:
        profiles = update_profile_by_user_id(current_user, None, "", db)
    
        return profiles
    except ApiException as e:
        db.rollback()
        _logger.warning(f"request failed. status_code = {e.status_code} detail = {e.detail}")
        raise e

    except Exception as e:
        _logger.error(f"request failed. Error = {e}")
        print(e)
        db.rollback()
        raise ApiException(
                status_code=status.HTTP_400_BAD_REQUEST,
                status="fail",
                detail="BadRequest",
            )
    

@router.get("/ranks")
def get_ranks(db:Session = Depends(get_db)) -> Any:
    """
    ランクを取得する
    """
    try:
        profiles = get_all_ranks(db)
    
        return profiles
    except ApiException as e:
        db.rollback()
        _logger.warning(f"request failed. status_code = {e.status_code} detail = {e.detail}")
        raise e

    except Exception as e:
        _logger.error(f"request failed. Error = {e}")
        print(e)
        db.rollback()
        raise ApiException(
                status_code=status.HTTP_400_BAD_REQUEST,
                status="fail",
                detail="BadRequest",
            )
    

@router.get("/rank_table")
def get_rank_table(profile_id:str, rank_id:int, db:Session = Depends(get_db)) -> Any:
    """
    ランクを取得する
    """
    try:
        profiles = update_profile_rate(profile_id,rank_id,0,db)
    
        return profiles
    except ApiException as e:
        db.rollback()
        _logger.warning(f"request failed. status_code = {e.status_code} detail = {e.detail}")
        raise e

    except Exception as e:
        _logger.error(f"request failed. Error = {e}")
        print(e)
        db.rollback()
        raise ApiException(
                status_code=status.HTTP_400_BAD_REQUEST,
                status="fail",
                detail="BadRequest",
            )