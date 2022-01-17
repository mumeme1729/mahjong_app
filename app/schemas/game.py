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
    pass

class Game(GameBase):
    id: Optional[UUID] = None

    #データが辞書ではなくORMモデルであってもPydanticモデルとしてデータを読み取るようにする
    class Config:
        orm_mode = True