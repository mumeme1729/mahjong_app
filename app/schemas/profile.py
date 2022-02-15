from uuid import UUID
from xmlrpc.client import boolean
from pydantic import BaseModel
from typing import List, Optional


class ProfileBase(BaseModel):
    """
    profileの基本schema
    """
    is_active: Optional[bool] = None

class ProfileCreate(ProfileBase):
    """
    Profileの作成時のschema
    """
    nick_name: Optional[str] = None
    image: Optional[str] = None


class ProfileInDBBase(ProfileBase):
    id: Optional[UUID] = None

    #データが辞書ではなくORMモデルであってもPydanticモデルとしてデータを読み取るようにする
    class Config:
        orm_mode = True

class Profile(ProfileInDBBase):
    """
    API経由時に追加するプロパティ
    """
    pass

