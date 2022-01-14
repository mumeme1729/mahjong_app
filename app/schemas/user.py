from uuid import UUID
from sqlalchemy.sql.sqltypes import TIMESTAMP
from sqlalchemy.sql.type_api import UserDefinedType
from sqlalchemy.orm import Session
from schemas.group import Group
from sqlalchemy_utils import UUIDType
from pydantic import BaseModel,EmailStr
from typing import Optional,List
from datetime import datetime
from models.users import UserTable

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

class UserInDBBase(UserBase):
    id: Optional[UUID] = None

    class Config:
        orm_mode = True

class User(UserInDBBase):
    """
    API経由時に追加するプロパティ
    """

    groups: List[Group]

class UserInDB(UserInDBBase):
    """
    DB保存時に追加するプロパティ
    """
    hashed_password:str





        

