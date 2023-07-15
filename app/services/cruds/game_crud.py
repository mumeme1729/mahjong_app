
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
    try:
        game = GamesTable(
            created_at = game_data.date,
            update_at = game_data.date,
            is_sanma = game_data.is_sanma,
            group_id = game_data.group_id,
            creater = profile.id
        )

        db.add(game)
        db.commit()
        return game.id
    except Exception as e:
            raise e

def update_game_and_result(game_data:GameUpdata,profile:ProfileTable,db:Session):
    """
    ゲームテーブルを更新する
    """
    try:
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
    except Exception as e:
            raise e



def get_game_by_id(game_id:UUID,db:Session)->GamesTable:
    """
    対象のゲームをidから検索
    """
    try:
        return db.query(GamesTable).options(joinedload(GamesTable.game_results)).filter(GamesTable.id == game_id).first()
    except Exception as e:
        raise e

def get_recently_game(group_id,db:Session):
    """
    指定したグループの直近の対局記録を取得数する
    """
    try:
        # game = db.query(GamesTable).\
        #     options(joinedload(GamesTable.game_results)).\
        #         filter(GamesTable.group_id == group_id).limit(10).all()
        get_recently_gameresult_query = f"""
            SELECT 
                games.id, games.is_sanma, games.created_at,
                gameresults.score, gameresults.rank,
                profiles.nick_name 
            FROM games
            LEFT JOIN gameresults ON games.id = gameresults.game
            LEFT JOIN profiles ON profiles.id = gameresults.profile
            WHERE games.group_id = '{group_id}'
            ORDER BY games.created_at DESC, gameresults.rank ASC
            LIMIT 50;
        """
        LIMIT = 8
        game_results = db.execute(get_recently_gameresult_query)
        game_results_dict:dict = {}
        for res in game_results:
            result_dict = dict(res)
            if len(game_results_dict) <= LIMIT:
                game_results_dict.setdefault(result_dict.get("id"),[]).append(res)
                if len(game_results_dict) > LIMIT:
                     game_results_dict.pop(result_dict.get("id"))
                     break
            else:
                 break
        return game_results_dict
    except Exception as e:
            print(e)
            raise e

def get_gams_within_specified_period(group_id:str,date_from:str,date_until:str,db:Session):
    """
    指定したグループの指定期間内の対局記録を取得数する
    """
    try:
        # game = db.query(GamesTable).\
        #     options(joinedload(GamesTable.game_results)).\
        #         filter(GamesTable.group_id == group_id).limit(10).all()grg
        get_recently_gameresult_query = f"""
            SELECT 
                games.id, games.is_sanma, games.created_at,
                gameresults.score, gameresults.rank,
                profiles.nick_name 
            FROM games
            LEFT JOIN gameresults ON games.id = gameresults.game
            LEFT JOIN profiles ON profiles.id = gameresults.profile
            WHERE games.group_id = '{group_id}'
            AND games.is_sanma = false
            AND games.created_at BETWEEN '{date_from}' AND '{date_until}'
            ORDER BY games.created_at DESC, gameresults.rank ASC
            LIMIT 20
        """
        game_results = db.execute(get_recently_gameresult_query)
        game_results_dict:dict = {}
        for res in game_results:
            result_dict = dict(res)
            game_results_dict.setdefault(result_dict.get("id"),[]).append(res)
                
        return game_results_dict
    except Exception as e:
            print(e)
            raise e

def get_games_orderby_date(group_id,db:Session):
    """
    指定したグループの直近の対局記録を取得数する
    """
    try:
        # game = db.query(GamesTable).\
        #     options(joinedload(GamesTable.game_results)).\
        #         filter(GamesTable.group_id == group_id).limit(10).all()
        get_recently_gameresult_query = f"""
            SELECT 
                games.id, games.is_sanma, games.created_at,
                gameresults.score, gameresults.rank,
                profiles.nick_name 
            FROM games
            LEFT JOIN gameresults ON games.id = gameresults.game
            LEFT JOIN profiles ON profiles.id = gameresults.profile
            WHERE games.group_id = '{group_id}'
            AND games.is_sanma = false
            ORDER BY games.created_at DESC, gameresults.rank ASC
            LIMIT 50;
        """
        LIMIT = 8
        game_results = db.execute(get_recently_gameresult_query)
        game_results_dict:dict = {}
        for res in game_results:
            result_dict = dict(res)
            if len(game_results_dict) <= LIMIT:
                game_results_dict.setdefault(result_dict.get("id"),[]).append(res)
                if len(game_results_dict) > LIMIT:
                     game_results_dict.pop(result_dict.get("id"))
                     break
            else:
                 break
        return game_results_dict
    except Exception as e:
            print(e)
            raise e

def get_recently_game2(group_id,db:Session):
    """
    指定したグループの直近の対局記録を取得数する
    """
    try:
        game = db.query(GamesTable).\
            options(joinedload(GamesTable.game_results)).\
                filter(GamesTable.group_id == group_id).limit(10).all()

        print(game.game_results)
        # game_results = db.execute(get_recently_gameresult_query)
        # game_results_dict=[]
        # for res in game_results:
        #     result_dict = dict(res)
        #     game_results_dict.append(result_dict)
        return game
    except Exception as e:
            print(e)
            raise e

### DELETE ###
def delete_game(game_id:UUID,db:Session):
    """
    対象の対局を削除する
    """
    try:
        target_game = get_game_by_id(game_id,db)
        if target_game is None:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="this game does not exist",
            )
        db.delete(target_game)
        db.commit()
        return target_game.id
    except Exception as e:
        raise e
