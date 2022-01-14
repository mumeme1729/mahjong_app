"""
groupのCRUD処理を実装

"""

from typing import List
from uuid import UUID
from sqlalchemy.orm.session import Session
from sqlalchemy.sql.sqltypes import TIMESTAMP
from sqlalchemy.orm import joinedload
from sqlalchemy import and_
from schemas.group import GroupCreate
from services.cruds.user_crud import get_user_by_id
from schemas.user import UserInDBBase
from models.groups import GroupsTable
from services.logs.set_logs import set_logger
from fastapi import HTTPException
from utils import errors
from schemas.group import Group
from datetime import datetime, timedelta

 #ロガーの作成
_logger = set_logger(__name__)

#post
def set_group(group:GroupCreate,user:UserInDBBase,db:Session)->dict:
    """
    postされたgroup情報をDBに格納する
    """
    dt = datetime.now()
    dt.strftime("%Y/%m/%d %H:%M:%S")

    group = GroupsTable(
            title = group.title,
            password = group.password,
            text = group.text,
            image = group.image,
            created_at = dt,
            update_at = dt,
    )

    group.users.append(get_user_by_id(user.id,db))

    db.add(group)
    db.commit()
    return group

#update
def join_group(group_id:UUID,password:str,user_id:UUID,db:Session):
    """
    指定したグループに追加する
    パスワードが一致した場合に追加
    """
    target_group = get_group_by_id(group_id,db)
    if target_group:
        # passwordチェック
        if target_group.password != password:
            return "no match password"
        # 既に参加しているかどうかチェック
        user = get_user_by_id(user_id,db)
        if user in target_group.users:
            return "already joined"
        # グループに参加させる
        target_group.users.append(user)
        db.commit()
        return target_group
    else:
        return "no group"

#GET(idより)
def get_group_by_id(group_id:UUID,db:Session)-> GroupsTable:
    """
    idを複数受け取り、それに一致するグループをすべて返す
    """
    return db.query(GroupsTable).options(joinedload(GroupsTable.users)).filter(GroupsTable.id == group_id).first()


def get_all_groups(db:Session)->List[GroupsTable]:
    """
    すべてのグループを返す
    """
    groups = db.query(GroupsTable).options(joinedload(GroupsTable.users)).all()
    return groups

