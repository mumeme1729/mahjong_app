from sqlalchemy import Column,Integer,String,Boolean,TIMESTAMP
from sqlalchemy.sql.schema import ForeignKey
from sqlalchemy_utils import UUIDType
from sqlalchemy.orm import relationship
#from models.user_group_maps import UserGroupMapTable
from uuid import uuid4

from db import Base
from db import ENGINE

class RateTable(Base):
    """
    対局結果テーブル
    """
    __tablename__ = 'rates'
    id = Column(UUIDType(binary=False),primary_key=True,default=uuid4)
    created_at = Column(TIMESTAMP,nullable=False)
    update_at = Column(TIMESTAMP,nullable=False)
    rate4 = Column(Integer, default=1500)
    rate3 = Column(Integer, default=1800)
    
    # リレーション設定
    profile_id = Column(UUIDType(binary=False), ForeignKey('profiles.id'))


    
def main():
    # テーブルが存在しなければ、テーブルを作成
    Base.metadata.create_all(bind=ENGINE)


if __name__ == "__main__":
    main()