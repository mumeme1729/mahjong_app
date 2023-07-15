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


class ProfileBasicSchema(BaseModel):
    """
    profileの基本スキーマ
    レートとランクを含める
    """
    id: str
    is_active: bool
    created_at: str
    update_at: str
    nick_name: str
    image: str
    introduction: str
    group: str
    user: str
    rate4: int
    rate3: int
    rank_id: int
    rank_name: str
    point: int
    init_point: int
    pre_rank_id: int
    next_rank_id: int