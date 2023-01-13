
from typing import Any
import logging
from schemas.response import CommonResponseSuccess
import boto3
import config
from datetime import datetime
from utils.errors import ApiException
from fastapi import APIRouter, Depends, UploadFile, File
from sqlalchemy.orm import Session

from schemas.user import User, UserUpdate
from services.cruds.user_crud import get_all_user_data, update_user_crud
from services.cruds.user_crud import get_all_users, get_user_by_id
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
        user_data = get_all_user_data(current_user.id,db)
        # ユーザーデータを加工する
        nick_name:str = ""
        image:str = ""
        game_cnt:int = 0
        rank1:int = 0
        rank2:int = 0
        rank3:int = 0
        rank4:int = 0
        score:int = 0
        game_id = []
        group = []
        # return user_data

        for i in range(len(user_data)):
            # 最初のみ名前等を取得する
            if i == 0:
                nick_name = user_data[i]["UserTable"].nick_name
                image = user_data[i]["UserTable"].image
            if user_data[i]["ProfileTable"] is not None:
                for game_results in user_data[i]["ProfileTable"].game_results:
                    game_cnt += 1
                    score += game_results.score
                    if game_results.rank == 1:
                        rank1 += 1
                    elif game_results.rank == 2:
                        rank2 += 1
                    elif game_results.rank == 3:
                        rank3 += 1
                    else:
                        rank4 +=1
                    game_id.append(game_results.game)
            if user_data[i]["GroupsTable"] is not None:
                group.append(user_data[i]["GroupsTable"])
        # 参加しているすべてのグループを取得

        login_user ={
            "nick_name":nick_name,
            "image":image,
            "rank1":rank1,
            "rank2":rank2,
            "rank3":rank3,
            "rank4":rank4,
            "score":score,
            "game_cnt":game_cnt,
            "group":group
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
            s3 = boto3.client('s3',
                aws_access_key_id=config.AWS_ACCESS_KEY,
                aws_secret_access_key=config.AWS_SECRET_ACCESS_KEY,
                region_name=config.AWS_REGION
            )

            dt_now = datetime.now()
            dt = dt_now.strftime('%Y%m%d%H%M%S')
            filename = f"{current_user.id}_{dt}_{upload_file.filename}"
            Bucket = "mahjong-profile-image"
            Key = f'user_image/{filename}'
            s3.put_object(Body=upload_file.file, Bucket =Bucket, Key =Key)
            path = f"https://{Bucket}.s3-{config.AWS_REGION}.amazonaws.com/{Key}"
        #更新する
        if update_info.nick_name is None:
            update_info.nick_name = current_user.nick_name
        if update_info.introduction is None:
            update_info.introduction = current_user.introduction
            
        update_user_crud(current_user, update_info, path,db)
        return {"status":"ok"}
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
