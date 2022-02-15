
from uuid import UUID
from sqlalchemy.orm.session import Session
from datetime import datetime

from models.games_results import GameResultTable
from schemas.game_result import GameResultCreate

def set_game_result(game_id:UUID,game_result_data:GameResultCreate,db:Session)->dict:
    """
    対局結果を格納する
    """
    dt = datetime.now()
    dt.strftime("%Y/%m/%d %H:%M:%S")

    result = GameResultTable(
        created_at = dt,
        update_at = dt,
        rank = game_result_data.rank,
        score = game_result_data.score,
        game = game_id,
        profile = game_result_data.profile
    )

    db.add(result)
    db.commit()
    return result.id

