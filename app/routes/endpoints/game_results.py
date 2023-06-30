
from typing import Any, Optional
import logging
from services.cruds.game_result_crud import get_total_gameresults_per_profile
from services.cruds.game_result_crud import get_total_gameresults_per_user
from schemas.game_result import GrameGrade4
from utils.errors import ApiException
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from schemas.user import User
from services.cruds.user_crud import get_user_by_id
from services.logs.set_logs import set_logger
from services.authenticates.get_current_user import get_current_active_user
from db import get_db

router = APIRouter()

#ログファイルを作成
_logger = logging.getLogger(__name__)
set_logger(_logger)


@router.get("/login_user_total_gameresults4", response_model=GrameGrade4)
async def get_game_results(is_sanma:bool, profile_id:Optional[str]=None, current_user: User = Depends(get_current_active_user),db:Session = Depends(get_db)):
    """
    profile_id指定なし:ログインしているユーザーのトータル成績を取得する
    profile_id指定あり:profile_idのトータル成績を取得する
    """
    try:        
        game_result4_list = get_total_gameresults_per_user(current_user.id, is_sanma, db) if profile_id is None else get_total_gameresults_per_profile(profile_id, is_sanma, db)

        game_count:int = 0
        total_score:int = 0
        rank = { "1":0, "2":0, "3":0, "4":0 }
        for result in game_result4_list:
            game_count += result.get("count")
            total_score += result.get("sum")
            rank[str(result.get("rank"))] += result.get("count")
        rank1 = rank.get("1")
        rank2 = rank.get("2")
        rank3 = rank.get("3")
        rank4 = rank.get("4")
        grade4 = {
            "game_count": game_count,
            "rank1": rank1,
            "rank2": rank2,
            "rank3": rank3,
            "rank4": rank4,
            "total_score": total_score,
            "score_average": round(total_score/game_count, 1) if game_count != 0 else 0,
            "rank_average": round((rank1+rank2*2+rank3*3+rank4*4)/game_count, 1) if game_count != 0 else 0,
            "top_rate": round((rank1/game_count)*100, 1) if game_count != 0 else 0,
            "last_rate": round((rank4/game_count)*100, 1) if game_count != 0 else 0,
            "winning_rate":  round(((rank1+rank2)/game_count)*100, 1) if game_count != 0 else 0
        }
        
        return grade4
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
