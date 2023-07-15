from uuid import UUID
from models.profiles import ProfileTable
from pydantic import BaseModel,EmailStr
from typing import Optional,List

from schemas.profile import Profile
from models.users import UserTable


class UserBase(BaseModel):
    """
    userの基本schema
    """
    # email: Optional[EmailStr] = None
    firebase_uid: Optional[str] = None
    is_active: Optional[bool] = None

class UserCreate(UserBase):
    """
    user作成時のschema
    """
    # email: EmailStr
    # password: str
    firebase_uid: str

class UserUpdate(BaseModel):
    """
    UPDATE時のschema
    """
    # password: Optional[str] = None
    nick_name: Optional[str] = None
    introduction: Optional[str] = None

class UserUPdateProfiles(UserUpdate):
    """
    ユーザーに紐づくプロフィールを更新する際のスキーマ
    """
    nick_name: str
    introduction: str
    image: str


class UserInDBBase(UserBase):
    id: Optional[UUID] = None

    class Config:
        orm_mode = True

class User(UserInDBBase):
    """
    API経由時に追加するプロパティ
    """
    profiles: List[Profile]
    nick_name: Optional[str] = None
    introduction: Optional[str] = None
    image: Optional[str] = None

# class UserInDB(UserInDBBase):
#     """
#     DB保存時に追加するプロパティ
#     """
#     hashed_password:str

class LoginUserSchema():
    """
    ホーム画面表示用ユーザーデータスキーマ
    TODO
    """
    pass
    






        

