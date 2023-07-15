
from typing import Any
from uuid import UUID

import logging
from services.cruds.profile_crud import get_profile_by_profile_and_group


from utils.errors import ApiException
from fastapi import APIRouter, Depends,HTTPException,status
from sqlalchemy.orm import Session

from schemas.game import GameCreate
from schemas.user import User
from schemas.game import GameUpdata
from schemas.response import CommonResponseSuccess

from services.cruds.game_crud import update_game_and_result
from services.func.calc_rate import calc_rate_4, calc_rate_3
from services.cruds.profile_crud import get_profile_by_id
from services.cruds.group_crud import get_group_by_id
from services.cruds.game_result_crud import set_game_result
from services.cruds.game_crud import set_game, delete_game,get_game_by_id
from services.logs.set_logs import set_logger
from services.cruds.profile_crud import get_profile_by_user_and_group
from services.authenticates.get_current_user import get_current_active_user
from db import get_db

router = APIRouter()

#ログファイルを作成
_logger = logging.getLogger(__name__)
set_logger(_logger)

def create_game_results(game_data:GameCreate, group_id, game_id, db, is_sanma):
    if is_sanma:
        expected_results_length = 3
    else:
        expected_results_length = 4

    if len(game_data.game_results) != expected_results_length:
        delete_game(game_id, db)
        raise ApiException(
            status_code=status.HTTP_400_BAD_REQUEST,
            status="fail",
            detail="Illegal game result",
        )

    profiles = []
    for result in game_data.game_results:
        result.game = game_id
        prof = get_profile_by_profile_and_group(result.profile,group_id,db)

        if prof is None:
            delete_game(game_id, db)
            raise ApiException(
                status_code=status.HTTP_400_BAD_REQUEST,
                status="fail",
                detail="Invalid game result",
            )
        set_game_result(game_id, result, db)
        profiles.append(prof)

    return profiles


@router.post("/create_game", response_model=CommonResponseSuccess)
async def create_game(game_data: GameCreate, db: Session = Depends(get_db),
                      current_user: User = Depends(get_current_active_user)) -> Any:
    try:
        group = get_group_by_id(game_data.group_id, db)
        if not group:
            raise ApiException(
                status_code=status.HTTP_400_BAD_REQUEST,
                status="fail",
                detail=f"Group does not exist. : {game_data.group_id}",
            )

        profile = get_profile_by_user_and_group(current_user.id, group.id, db)
        if not profile or not profile.is_active:
            raise ApiException(
                status_code=status.HTTP_400_BAD_REQUEST,
                status="fail",
                detail="This user doesn't belong to this group or profile is not active.",
            )

        game_id = set_game(game_data, profile, db)
        profiles = create_game_results(game_data, group.id,game_id, db, game_data.is_sanma)

        try:
            calc_rate_4(game_data, profiles, db)
        except Exception as e:
            delete_game(game_id, db)
            raise e

        return {"status": "ok"}

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
