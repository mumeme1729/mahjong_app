
from typing import Any
import logging
from schemas.user import UserUPdateProfiles
from services.cruds.profile_crud import update_profile_by_user_id
from schemas.response import CommonResponseSuccess
import boto3
import config
from datetime import datetime
from utils.errors import ApiException
from fastapi import APIRouter, Depends, UploadFile, File
from sqlalchemy.orm import Session

from schemas.user import User, UserUpdate
from services.cruds.user_crud import get_all_users, get_user_by_id,update_user_crud,get_total_join_group_per_user
from services.logs.set_logs import set_logger
from services.authenticates.get_current_user import get_current_active_user
from db import get_db

router = APIRouter()

#ログファイルを作成
_logger = logging.getLogger(__name__)
set_logger(_logger)


@router.get("/me")#, response_model=User
async def read_users_me(current_user: User = Depends(get_current_active_user),db:Session = Depends(get_db)):
    """
    現在ログインしているユーザーを返す。
    """
    try:
        # ログインしているユーザー情報
        user_info = get_user_by_id(current_user.id, db)
        # ログインしているユーザーが参加しているグループ情報
        group_info_list:list = get_total_join_group_per_user(current_user.id,db)
       
        login_user ={
            "nick_name":user_info.nick_name,
            "image":user_info.image,
            "introduction":user_info.introduction,
            "group":group_info_list
        }
        
        return login_user
    except ApiException as e:
        db.rollback()
        _logger.warning(f"request failed. status_code = {e.status_code} detail = {e.detail}")
        raise e

    except Exception as e:
        _logger.error(f"request failed. Error = {e}")
        db.rollback()
        raise ApiException(
                status_code=400,
                status="fail",
                detail="BadRequest",
            )

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
    try:
        users = get_user_by_id(id,db)
        return users
    except ApiException as e:
        db.rollback()
        _logger.warning(f"request failed. status_code = {e.status_code} detail = {e.detail}")
        raise e

    except Exception as e:
        _logger.error(f"request failed. Error = {e}")
        db.rollback()
        raise ApiException(
                status_code=400,
                status="fail",
                detail="BadRequest",
            )


@router.put("/update_user_info", response_model = CommonResponseSuccess)
def update_user(update_info:UserUpdate= Depends(), upload_file:UploadFile = File(None), db:Session = Depends(get_db),current_user: User = Depends(get_current_active_user)):
    """
    ユーザー情報を更新する
    """
    try:
        # S3にUPロードする
        path = None
        if upload_file is not None:
            print(upload_file.filename)
            s3 = boto3.client('s3',
                aws_access_key_id=config.AWS_ACCESS_KEY,
                aws_secret_access_key=config.AWS_SECRET_ACCESS_KEY,
                region_name=config.AWS_REGION
            )

            dt_now = datetime.now()
            dt = dt_now.strftime('%Y%m%d%H%M%S')
            filename = f"{current_user.id}_{dt}_{upload_file.filename}"
            Bucket = "mahjong-profile-image"
            Key = f'user_image/{current_user.id}/{filename}'
            s3.put_object(Body=upload_file.file, Bucket =Bucket, Key =Key)
            path = f"https://{Bucket}.s3-{config.AWS_REGION}.amazonaws.com/{Key}"
        #更新する
        print(update_info)
        if update_info.nick_name is None:
            update_info.nick_name = current_user.nick_name
        if update_info.introduction is None:
            update_info.introduction = current_user.introduction
            
        update_user_crud(current_user, update_info, path,db)
        update_profile_info =  UserUPdateProfiles(
            nick_name=update_info.nick_name,
            introduction= update_info.introduction,
            image = path if upload_file is not None else current_user.image
        )
        # update_profile_info.nick_name = update_info.nick_name
        # update_profile_info.introduction = update_info.introduction
        # update_profile_info.image = path if upload_file is not None else current_user.image
        # プロフィールも同時に更新する
        print(update_profile_info)
        update_profile_by_user_id(current_user, update_profile_info, db)
    
        return {"status":"ok"}
    except ApiException as e:
        db.rollback()
        _logger.warning(f"request failed. status_code = {e.status_code} detail = {e.detail}")
        raise e

    except Exception as e:
        print(e)
        _logger.error(f"request failed. Error = {e}")
        db.rollback()
        raise ApiException(
                status_code=400,
                status="fail",
                detail="BadRequest",
            )
