from schemas.game_result import GameResultCreate
from pydantic import BaseModel
from typing import List, Optional
from uuid import UUID

class GameBase(BaseModel):
    """
    gameの基本schema
    """
    is_sanma: Optional[bool] = None

class GameCreate(GameBase):
    """
    Game作成時のschema
    """
    group_id: UUID
    is_sanma: bool
    date: str
    game_results:List[GameResultCreate]

class GameUpdata(GameBase):
    """
    Gameアップデート時のschema
    """
    id: Optional[UUID] = None
    group_id: UUID
    is_sanma: bool
    game_results:List[GameResultCreate]


    

class Game(GameBase):
    id: Optional[UUID] = None

    #データが辞書ではなくORMモデルであってもPydanticモデルとしてデータを読み取るようにする
    class Config:
        orm_mode = True