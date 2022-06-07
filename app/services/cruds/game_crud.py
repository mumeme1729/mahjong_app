
from tokenize import group
from uuid import UUID
from venv import create
from sqlalchemy.orm.session import Session
from datetime import datetime, timedelta
from schemas.game import GameUpdata
from models.profiles import ProfileTable
from models.games import GamesTable
from sqlalchemy.orm import joinedload

from schemas.game import GameCreate
from fastapi import HTTPException,status

def set_game(game_data:GameCreate,profile:ProfileTable,db:Session)->dict:
    """
    gameを作成してDBに格納する
    """
    dt = datetime.now()
    dt.strftime("%Y/%m/%d %H:%M:%S")

    game = GamesTable(
        created_at = dt,
        update_at = dt,
        is_sanma = game_data.is_sanma,
        group_id = game_data.group_id,
        creater = profile.id
    )

    db.add(game)
    db.commit()
    return game.id

def update_game_and_result(game_data:GameUpdata,profile:ProfileTable,db:Session):
    """
    ゲームテーブルを更新する
    """
    #対象のゲームを取得
    game = get_game_by_id(game_data.id,db)

    dt = datetime.now()
    dt.strftime("%Y/%m/%d %H:%M:%S")
    game.update_at = dt
    game.updater = profile.id

    # アップデートする情報
    for update_result in game_data.game_results:
        # アップデート前の情報
        for pre_result in game.game_results:
            # プロフィールが一致した場合更新する
            if(pre_result.profile == update_result.profile):
                pre_result.rank = update_result.rank
                pre_result.score = update_result.score
                pre_result.update_at = dt

    db.commit()
    return game.id       



def get_game_by_id(game_id:UUID,db:Session)->GamesTable:
    """
    対象のゲームをidから検索
    """
    return db.query(GamesTable).options(joinedload(GamesTable.game_results)).filter(GamesTable.id == game_id).first()

def get_recently_game(group_id,db:Session):
    """
    指定したグループの直近のデータを取得
    """
    game = db.query(GamesTable).\
        options(joinedload(GamesTable.game_results)).\
            filter(GamesTable.group_id == group_id).limit(10).all()
    
    return game

### DELETE ###
def delete_game(game_id:UUID,db:Session):
    """
    対象の対局を削除する
    """
    target_game = get_game_by_id(game_id,db)
    if target_game is None:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="this game does not exist",
        )
    db.delete(target_game)
    db.commit()
    return target_game.id
