
from typing import Any
from uuid import UUID
import yaml
from schemas.response import CommonResponseSuccess
from utils.errors import ApiException

from services.cruds.game_crud import update_game_and_result
from schemas.game import GameUpdata

from fastapi import APIRouter, Depends,HTTPException,status
from sqlalchemy.orm import Session

from schemas.game import GameCreate
from schemas.user import User


import logging
from services.cruds.group_crud import get_group_by_id
from services.cruds.game_result_crud import set_game_result
from services.cruds.game_crud import set_game, delete_game,get_game_by_id
from services.logs.set_logs import set_logger
from services.cruds.profile_crud import get_profile_by_user_and_group
from services.authenticates.get_current_user import get_current_active_user
from db import get_db

router = APIRouter()

with open('settings.yaml', 'r') as yml:
    settings = yaml.safe_load(yml)

#ログファイルを作成
_logger = logging.getLogger(__name__)
set_logger(_logger)


@router.post("/create_game", response_model = CommonResponseSuccess)
async def create_game(game_data:GameCreate,db:Session = Depends(get_db),current_user: User = Depends(get_current_active_user))->Any:
    """
    対局テーブルを作成する
    """
    try:
        _logger.info(f"get current user : {current_user.id}")
        # グループのチェック
        group = get_group_by_id(game_data.group_id,db)
        # グループが存在しない場合はBAD_REQUEST
        if not group:
            raise ApiException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    status="fail",
                    detail=f"Group does not exist. : {game_data.group_id}",
                )
        # そのグループにPOSTしたユーザーが属しているか
        # プロフィールを取得
        profile = get_profile_by_user_and_group(current_user.id,group.id,db)
        if profile is not None:
            #そのプロフィールが有効かどうかチェック
            if profile.is_active:
                game_id = set_game(game_data,profile,db) #作成したゲームID
                #対局作成後、対局結果を格納していく
                #四麻か秋刀魚か判定
                if not game_data.is_sanma:
                    # 対局数をチェック
                    if len(game_data.game_results) == 4:
                        for result in game_data.game_results:
                            result.game = game_id
                            #結果を格納する
                            #TODO プロフィールチェック 
                            gr = set_game_result(game_id,result,db)
                    else:
                        # 対象のゲームを削除する
                        delete_game(game_id,db)
                        raise ApiException(
                            status_code=status.HTTP_400_BAD_REQUEST,
                            status="fail",
                            detail="Illegal game result",
                        )
                else:
                    # 秋刀魚
                    if len(game_data.game_results) == 3:
                        #結果を格納する
                        for result in game_data.game_results:
                            result.game = game_id
                            #結果を格納する
                            gr = set_game_result(game_id,result,db)
                    else:
                        # 不正なため対象のゲームを削除する
                        delete_game(game_id,db)
                        raise ApiException(
                            status_code=status.HTTP_400_BAD_REQUEST,
                            status="fail",
                            detail="Illegal game result",
                        )
                return {"status":"ok"}
        raise ApiException(
                status_code=status.HTTP_400_BAD_REQUEST,
                status="fail",
                detail="this user doesn't belong to this group.",
            )

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

@router.delete("/delete_game", response_model = CommonResponseSuccess)
def delete_game_table(game_id:UUID,db:Session = Depends(get_db),current_user: User = Depends(get_current_active_user))->Any:
    """
    対象の対局を削除する
    """
    try:
        res = delete_game(game_id,db)
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

@router.get("/get_game")
def get_game(game_id:UUID,db:Session = Depends(get_db),current_user: User = Depends(get_current_active_user)):
    try:
        res = get_game_by_id(game_id,db)
        return res
    except ApiException as e:
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

@router.put("/update_game", response_model = CommonResponseSuccess)
def update_game(game_data:GameUpdata,db:Session = Depends(get_db),current_user: User = Depends(get_current_active_user)):
    try:
        # グループのチェック
        group = get_group_by_id(game_data.group_id,db)
        # グループが存在しない場合はBAD_REQUEST
        if not group:
            raise ApiException(
                status_code=status.HTTP_400_BAD_REQUEST,
                status="fail",
                detail=f"Group does not exist. : {game_data.group_id}",
            )
        # プロフィールを取得
        profile = get_profile_by_user_and_group(current_user.id,group.id,db)
        if profile is not None:
            # アップデートを行う
            res = update_game_and_result(game_data,profile,db)
            return {"status":"ok"}    
        raise ApiException(
                status_code=status.HTTP_400_BAD_REQUEST,
                status="fail",
                detail=f"this user doesn't belong to this group.",
            )

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
