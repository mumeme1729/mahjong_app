from pydantic import BaseModel
from typing import List, Optional
from uuid import UUID

class GameResultBase(BaseModel):
    """
    gameResultの基本schema
    """
    rank: Optional[int]
    score: Optional[int]

class GameResultCreate(GameResultBase):
    """
    game作成時のschema
    """
    rank: int
    score: int
    game: Optional[UUID]
    profile: str
