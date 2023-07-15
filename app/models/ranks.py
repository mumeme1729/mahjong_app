from sqlalchemy import Column,Integer,String,Boolean,TIMESTAMP
from sqlalchemy.sql.schema import ForeignKey
from sqlalchemy_utils import UUIDType
from sqlalchemy.orm import relationship
#from models.user_group_maps import UserGroupMapTable
from uuid import uuid4

from db import Base
from db import ENGINE

class RankTable(Base):
    """
    対局結果テーブル
    """
    __tablename__ = 'ranks'
    id = Column(Integer,primary_key=True)
    rank_name =  Column(String(30))
    point = Column(Integer)
    init_point = Column(Integer)
    pre_rank_id = Column(Integer)
    next_rank_id = Column(Integer)
    
def main():
    # テーブルが存在しなければ、テーブルを作成
    Base.metadata.create_all(bind=ENGINE)


if __name__ == "__main__":
    main()