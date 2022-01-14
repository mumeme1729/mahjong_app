from uuid import UUID
from sqlalchemy.sql.sqltypes import TIMESTAMP
from sqlalchemy.sql.type_api import UserDefinedType
from sqlalchemy.orm import Session
from sqlalchemy_utils import UUIDType
from pydantic import BaseModel,EmailStr
from typing import List, Optional
from datetime import datetime
from models.groups import GroupsTable


class GroupBase(BaseModel):
    """
    groupの基本schema
    """
    # id: int
    title: Optional[str] = None
    password: Optional[str] = None
    text: Optional[str] = None
    image: Optional[str] = None
    # created_at: datetime
    # update_at: datetime

class GroupCreate(GroupBase):
    """
    Groupの作成時のschema
    """
    title: str
    password: str


class GroupInDBBase(GroupBase):
    id: Optional[UUID] = None

    #データが辞書ではなくORMモデルであってもPydanticモデルとしてデータを読み取るようにする
    class Config:
        orm_mode = True

class Group(GroupInDBBase):
    """
    API経由時に追加するプロパティ
    """
    pass

class GroupInDB(GroupInDBBase):
    """
    DB保存時に追加するプロパティ
    """
    pass

