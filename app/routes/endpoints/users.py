from typing import Any
import yaml

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from schemas.user import User
from services.cruds.user_crud import get_all_user_data
from services.cruds.user_crud import get_all_users, get_user_by_id
from services.logs.set_logs import set_logger
from services.authenticates.get_current_user import get_current_active_user
from db import get_db

router = APIRouter()

with open('settings.yaml', 'r') as yml:
    settings = yaml.safe_load(yml)

#ログファイルを作成
_uvicorn_accsess_logger = set_logger("uvicorn.access",file_name = 'access')
_ormapper_logger = set_logger("sqlalchemy.engine",file_name='ormapper')
_logger = set_logger(__name__)


@router.get("/me/")#, response_model=User
async def read_users_me(current_user: User = Depends(get_current_active_user),db:Session = Depends(get_db)):
    """
    現在ログインしているユーザーを返す。
    """
    _logger.info(f"get current user : {current_user.email}")
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
    login_user ={
        "nick_name":nick_name,
        "image":image,
        "rank1":rank1,
        "rank2":rank2,
        "rank3":rank3,
        "rank4":rank4,
        "score":score,
        "game_cnt":game_cnt
    }
    
    return login_user

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
    users = get_user_by_id(id,db)
    return users