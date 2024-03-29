from sqlalchemy import Column,Integer,String,Boolean,TIMESTAMP,UniqueConstraint
from sqlalchemy_utils import UUIDType
from sqlalchemy.orm import relationship
from sqlalchemy.sql.schema import ForeignKey
from uuid import uuid4
#from models.user_group_maps import UserGroupMapTable
#from .profile_group_maps import profile_group_map_table
from db import Base
from db import ENGINE

class ProfileTable(Base):
    """
    プロフィールテーブル
    グループごとに作成する
    """
    __tablename__ = 'profiles'
    __table_args__ = (UniqueConstraint('user','group'),{})
    id = Column(UUIDType(binary=False),primary_key=True,default=uuid4)
    is_active = Column(Boolean,nullable=False, default=True)
    created_at = Column(TIMESTAMP,nullable=False)
    update_at = Column(TIMESTAMP,nullable=False)
    nick_name = Column(String(30))
    image = Column(String(255))

    introduction = Column(String(1000))

    #所属しているグループ情報

    # リレーション設定
    group = Column(UUIDType(binary=False), ForeignKey('groups.id'))
    user = Column(UUIDType(binary=False), ForeignKey('users.id'))
    game_results = relationship("GameResultTable", backref="profiles")
    rate = relationship("RateTable", backref="profiles")
    # rate = profile_id = Column(UUIDType(binary=False), ForeignKey('rates.id'))
    
def main():
    # テーブルが存在しなければ、テーブルを作成
    Base.metadata.create_all(bind=ENGINE)


if __name__ == "__main__":
    main()