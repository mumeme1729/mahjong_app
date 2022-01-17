from sqlalchemy import Column,Integer,String,Boolean,TIMESTAMP
from sqlalchemy.sql.schema import ForeignKey
from sqlalchemy_utils import UUIDType
from sqlalchemy.orm import relationship
#from models.user_group_maps import UserGroupMapTable
from models.user_group_maps import user_group_map_table
from uuid import uuid4

from db import Base
from db import ENGINE

class GamesTable(Base):
    """
    対局テーブル
    """
    __tablename__ = 'games'
    id = Column(UUIDType(binary=False),primary_key=True,default=uuid4)
    created_at = Column(TIMESTAMP,nullable=False)
    update_at = Column(TIMESTAMP,nullable=False)
    is_sanma = Column(Boolean,nullable=False, default=False)

    # リレーション設定
    group_id = Column(UUIDType(binary=False), ForeignKey('groups.id'))

    
def main():
    # テーブルが存在しなければ、テーブルを作成
    Base.metadata.create_all(bind=ENGINE)


if __name__ == "__main__":
    main()