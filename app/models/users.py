from sqlalchemy import Column,Integer,String,Boolean,TIMESTAMP
from sqlalchemy_utils import UUIDType
from sqlalchemy.orm import relationship
from uuid import uuid4
#from models.user_group_maps import UserGroupMapTable
from .user_group_maps import user_group_map_table
from db import Base
from db import ENGINE

class UserTable(Base):
    """
    ユーザーテーブル
    """
    __tablename__ = 'users'
    id = Column(UUIDType(binary=False),primary_key=True,default=uuid4)
    email = Column(String(30),unique=True,nullable=False)
    hashed_password = Column(String(255),nullable=False)
    is_active = Column(Boolean,nullable=False, default=True)
    created_at = Column(TIMESTAMP,nullable=False)
    #所属しているグループ情報

    # リレーション設定
    groups = relationship(
        'GroupsTable',
        secondary= user_group_map_table,
        back_populates='users'
    )
    
def main():
    # テーブルが存在しなければ、テーブルを作成
    Base.metadata.create_all(bind=ENGINE)


if __name__ == "__main__":
    main()