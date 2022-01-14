"""
userとgroupを結びつける中間テーブル
"""

from sqlalchemy import Column,Integer,String,Boolean,TIMESTAMP,ForeignKey,Table
from sqlalchemy_utils import UUIDType
from sqlalchemy.orm import relationship
from uuid import uuid4
from db import Base
from db import ENGINE


user_group_map_table = Table(
    'user_group_map_table',
    Base.metadata,
    Column('group_id',UUIDType(binary=False),ForeignKey('groups.id'),primary_key=True),
    Column('user_id',UUIDType(binary=False),ForeignKey('users.id'),primary_key=True)
)
