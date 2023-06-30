
from uuid import UUID
from sqlalchemy.orm.session import Session
from datetime import datetime
from typing import List
from models.games_results import GameResultTable
from schemas.game_result import GameResultCreate

def set_game_result(game_id:UUID,game_result_data:GameResultCreate,db:Session)->dict:
    """
    対局結果を格納する
    """
    try:
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
    except Exception as e:
            raise e


def get_total_gameresults_per_profile(profile_id: str, is_sanma:bool, db: Session)->List[dict]:
    """
    指定されたプロフィールの全対局結果の集計を返す
    """
    try:
        get_game_result_query = f"""
            SELECT gameresults.rank, COUNT(*), SUM(gameresults.score) FROM profiles
            JOIN gameresults ON profiles.id = gameresults.profile
            JOIN games ON games.id = gameresults.game
            WHERE profiles.id::text = '{profile_id}'
            AND games.is_sanma = {is_sanma}
            GROUP BY gameresults.rank, gameresults.score;
        """
        game_results = db.execute(get_game_result_query)

        game_results_list = []
        for res in game_results:
            result_dict = dict(res)
            game_results_list.append(result_dict)
        print(f"profile = {game_results_list}")
        return game_results_list
    
    except Exception as e:
            raise e


def get_total_gameresults_per_user(user_id: str, is_sanma:bool, db: Session)->List[dict]:
    """
    指定されたユーザーの全対局結果の集計を返す
    """
    try:
        get_game_result_query = f"""
            SELECT gameresults.rank, COUNT(*), SUM(gameresults.score) FROM users
            JOIN profiles ON users.id = profiles.user
            JOIN gameresults ON profiles.id = gameresults.profile
            JOIN games ON games.id = gameresults.game
            WHERE users.id::text = '{user_id}'
            AND games.is_sanma = {is_sanma}
            GROUP BY gameresults.rank, gameresults.score;
        """
        game_results = db.execute(get_game_result_query)

        game_results_list = []
        for res in game_results:
            result_dict = dict(res)
            game_results_list.append(result_dict)

        return game_results_list
    
    except Exception as e:
            raise e