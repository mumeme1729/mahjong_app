from uuid import UUID
from pydantic import BaseModel,EmailStr
from typing import Optional,List

from schemas.profile import Profile


class UserBase(BaseModel):
    """
    userの基本schema
    """
    email: Optional[EmailStr] = None
    is_active: Optional[bool] = None

class UserCreate(UserBase):
    """
    user作成時のschema
    """
    email: EmailStr
    password: str

class UserUpdate(UserBase):
    """
    UPDATE時のschema
    """
    password: Optional[str] = None
    nick_name: Optional[str] = None
    image: Optional[str] = None


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
    image: Optional[str] = None

class UserInDB(UserInDBBase):
    """
    DB保存時に追加するプロパティ
    """
    hashed_password:str





        

