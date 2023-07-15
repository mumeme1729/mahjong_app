from email.mime import image
from typing import List, Optional
from uuid import UUID
from sqlalchemy.orm.session import Session
from sqlalchemy.orm import joinedload
from schemas.profile import ProfileBasicSchema
from models.ranks import RankTable
from schemas.user import UserUPdateProfiles
from schemas.user import UserUpdate
from models.rate import RateTable
from schemas.user import User
from datetime import datetime

from models.profiles import ProfileTable

def get_all_ranks(db: Session):
     """
     全てのランクを取得する
     """
     try:
        ranks = db.query(RankTable).all()
        return ranks
     except Exception as e:
        raise e

def get_rank_by_rankid(rank_id:int, db: Session)->Optional[RankTable]:
     """
     特定のランクを取得する
     """
     try:
        rank = db.query(RankTable).filter(RankTable.id == rank_id).first()
        return rank
     except Exception as e:
        raise e
     
    