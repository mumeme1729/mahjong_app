
from tokenize import group
from sqlalchemy.orm.session import Session
from datetime import datetime, timedelta
from models.games import GamesTable

from schemas.user import UserInDBBase
from schemas.game import GameCreate

def set_game(game_data:GameCreate,db:Session)->dict:
    """
    gameを作成してDBに格納する
    """
    dt = datetime.now()
    dt.strftime("%Y/%m/%d %H:%M:%S")

    game = GamesTable(
        created_at = dt,
        update_at = dt,
        is_sanma = game_data.is_sanma,
        group_id = game_data.group_id
    )

    db.add(game)
    db.commit()
    return game