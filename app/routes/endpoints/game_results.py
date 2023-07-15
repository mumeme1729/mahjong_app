
from datetime import datetime, timedelta
from typing import Any, List, Optional
import logging
from services.cruds.game_result_crud import get_tobi_count_per_profile
from services.cruds.profile_crud import get_profile_by_id_with_rate
from services.cruds.game_result_crud import get_maxmin_score_per_profile
from services.cruds.game_result_crud import get_recent_recent_gamerank_per_profile
from services.cruds.profile_crud import get_profile_by_id
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
async def get_game_results(is_sanma:bool, current_user: User = Depends(get_current_active_user),db:Session = Depends(get_db)):
    """
    profile_id指定なし:ログインしているユーザーのトータル成績を取得する
    """
    try:        
        game_result4_list = get_total_gameresults_per_user(current_user.id, is_sanma, db)

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


@router.post("/profile_total_game_grade4")
async def get_game_results_per_profile(is_sanma:bool, profile_ids:List[str], date_from:str, date_until:str, current_user: User = Depends(get_current_active_user),db:Session = Depends(get_db)):
    """
    profile_idsで受け取ったプロフィールの指定された期間のデータを返す
    """
    try:
        response_list = []
        for profile_id in profile_ids:
            # プロフィールに基づく対局結果取得
            game_result4_list =  get_total_gameresults_per_profile(profile_id, is_sanma,date_from,date_until,db)
            # プロフィールの詳細取得
            profile_info = get_profile_by_id(profile_id, db)
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
                "id": profile_info.id,
                "nick_name": profile_info.nick_name,
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
            response_list.append(grade4)
        return response_list
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


@router.get("/personal_record_per_profile")
async def get_personal_record_per_profile(is_sanma:bool, profile_id:str, current_user: User = Depends(get_current_active_user),db:Session = Depends(get_db)):
    """
    profile_idで受け取ったプロフィールの個人戦績を返す
    """
    try:
        date_from = "2020/04/07 11:15"
        dt = datetime.now() + timedelta(days=1)
        dt.strftime("%Y/%m/%d %H:%M:%S")
        date_until = dt
        # プロフィールに基づく対局結果取得
        game_result4_list =  get_total_gameresults_per_profile(profile_id, is_sanma,date_from,date_until,db)
        # プロフィールの詳細取得(レートも含める)
        profile_info = get_profile_by_id_with_rate(profile_id, db)
        # 直近の順位
        racent_rank = get_recent_recent_gamerank_per_profile(profile_id, is_sanma, db)
        # 得点の最大最小値
        maxmin_score = get_maxmin_score_per_profile(profile_id, is_sanma, db)
        # 飛び率
        tobi_count = get_tobi_count_per_profile(profile_id, is_sanma, db)
        tobi = tobi_count.get("tobi_count") if tobi_count.get("tobi_count") is not None else 0
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
            "id": profile_info.id,
            "nick_name": profile_info.nick_name,
            "introduction":profile_info.introduction,
            "image": profile_info.image,
            "recent_rank":racent_rank,
            "max_score_origin": maxmin_score.get("max_score_origin"),
            "min_score_origin": maxmin_score.get("min_score_origin"),
            "rank_name":profile_info.rank_name,
            "rate4": profile_info.rate4,
            "point": profile_info.point,
            "tobi_count":tobi_count,
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
            "winning_rate":  round(((rank1+rank2)/game_count)*100, 1) if game_count != 0 else 0,
            "tobi_rate": round(((tobi)/game_count)*100, 1) if game_count != 0 else 0
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