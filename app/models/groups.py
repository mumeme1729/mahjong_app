from sqlalchemy import Column,Integer,String,Boolean,TIMESTAMP
from sqlalchemy.sql.schema import ForeignKey
from sqlalchemy_utils import UUIDType
from sqlalchemy.orm import relationship
#from models.user_group_maps import UserGroupMapTable
from models.user_group_maps import user_group_map_table
from uuid import uuid4

from db import Base
from db import ENGINE

class GroupsTable(Base):
    """
    グループテーブル
    """
    __tablename__ = 'groups'
    id = Column(UUIDType(binary=False),primary_key=True,default=uuid4)
    title = Column(String(30),unique=True,nullable=False)
    password = Column(String(255),nullable=False)
    text = Column(String(255))
    image = Column(String(255))
    created_at = Column(TIMESTAMP,nullable=False)
    update_at = Column(TIMESTAMP,nullable=False)

    # リレーション設定
    users = relationship(
        'UserTable',
        secondary= user_group_map_table,
        back_populates='groups'
    )

    
def main():
    # テーブルが存在しなければ、テーブルを作成
    Base.metadata.create_all(bind=ENGINE)


if __name__ == "__main__":
    main()