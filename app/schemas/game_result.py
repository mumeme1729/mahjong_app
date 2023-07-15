from pydantic import BaseModel
from typing import List, Optional
from uuid import UUID

class GameResultBase(BaseModel):
    """
    gameResultの基本schema
    """
    rank: Optional[int]
    score: Optional[int]
    score_origin: Optional[int]

class GameResultCreate(GameResultBase):
    """
    game作成時のschema
    """
    rank: int
    score: int
    score_origin: int
    game: Optional[UUID]
    profile: str

class GrameGrade4(BaseModel):
    """
    4人麻雀成績スキーマ
    """
    game_count:int
    rank1:int
    rank2:int
    rank3:int
    rank4:int
    total_score:int
    score_average:float
    rank_average:float
    top_rate:float
    last_rate:float
    winning_rate:float

class GrameGrade3(BaseModel):
    """
    3人麻雀成績スキーマ
    """
    game_count:int
    rank1:int
    rank2:int
    rank3:int
    score_sum:int
