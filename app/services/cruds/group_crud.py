"""
profileのCRUD処理を実装

"""

from typing import List
from uuid import UUID
from sqlalchemy.orm.session import Session
from sqlalchemy.orm import joinedload
from schemas.group import GroupInfoUpdate
from models.profiles import ProfileTable
from utils.errors import ApiException
from services.cruds.game_crud import get_recently_game
from services.cruds.profile_crud import dis_activate_profile
from services.cruds.profile_crud import activate_profile
from models.games import GamesTable
from services.cruds.profile_crud import get_profile_by_user_and_group, set_profile
from services.cruds.profile_crud import get_profile_by_user_id,get_profile_by_id
from schemas.group import GroupCreate
from services.cruds.user_crud import get_user_by_id
from schemas.user import User
from models.groups import GroupsTable
from fastapi import HTTPException,status
from datetime import datetime


#post
def set_group(group:GroupCreate,user:User,db:Session)->dict:
    """
    postされたgroup情報をDBに格納する
    """
    try:
        dt = datetime.now()
        dt.strftime("%Y/%m/%d %H:%M:%S")

        group = GroupsTable(
                title = group.title,
                password = group.password,
                text = group.text,
                created_at = dt,
                update_at = dt
        )

        #group.users.append(get_user_by_id(user.id,db))

        db.add(group)
        db.commit()
        return group.id
    except Exception as e:
            raise e

#update
def join_group(group_id:UUID,password:str,user_id:UUID,db:Session)->UUID:
    """
    指定したグループに追加する
    パスワードが一致した場合に追加
    """
    try:
        target_group = get_group_by_id(group_id,db)
        if target_group:
            # passwordチェック
            if target_group.password != password:
                raise ApiException(
                    status_code=status.HTTP_401_UNAUTHORIZED,
                    status="fail",
                    detail="Password does not match",
                )
            # 既に参加しているかどうかチェック
            profile = get_profile_by_user_and_group(user_id,target_group.id,db)
            if profile is not None:
                if profile.is_active:
                    # 既に参加している場合
                    raise ApiException(
                        status_code=status.HTTP_400_BAD_REQUEST,
                        status="fail",
                        detail="already joined this group",
                    )
                else:
                    # プロフィールを有効化させる
                    res = activate_profile(profile,db)
                    if res: 
                        return target_group.id
            
            # グループに参加させる
            # profileを作成
            user = get_user_by_id(user_id,db)
            if user is None:
                raise  ApiException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    status="fail",
                    detail="user does not exists.",
                )
            profile_id = set_profile(user, group_id, db)
            if profile_id is None:
                raise  ApiException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    status="fail",
                    detail="Cloud not create user profile",
                )
            db.commit()
            return profile_id
        else:
            return ApiException(
                status_code=status.HTTP_400_BAD_REQUEST,
                status="fail",
                detail="Group does not exist",
            )
    except ApiException as e:
        raise e
    
    except Exception as e:
            raise e

def update_group_image(group_id:UUID, image_path:str ,db:Session):
    """
    グループのイメージを更新する
    """
    try:
        group =  get_group_by_id(group_id, db)
        group.image = image_path
        db.commit()
        return group.id
    except Exception as e:
        raise e
    

#GET(idより)
def get_group_by_id(group_id:UUID,db:Session)-> GroupsTable:
    """
    idを複数受け取り、それに一致するグループを返す
    """
    try:
        return db.query(GroupsTable).options(joinedload(GroupsTable.profiles)).filter(GroupsTable.id == group_id).first()
    except Exception as e:
            raise e

def get_all_groups(db:Session)->List[GroupsTable]:
    """
    すべてのグループを返す
    """
    try:
        groups = db.query(GroupsTable).options(joinedload(GroupsTable.profiles)).options(joinedload(GroupsTable.games)).all()
        # get_group_query = f"""
        #     SELECT profiles.*, rates.rate4, rates.rate3 FROM profiles
        #     JOIN rates ON profiles.id = rates.profile_id
        #     WHERE profiles.group = '3ada6498-1e48-4e96-8603-925c18ecd3f9';
        # """
        # groups = db.execute(get_group_query)
        return groups
    except Exception as e:
            print(e)
            raise e

def get_selected_group(group_id:str,db:Session)->GroupsTable:
    """
    選択したグループの情報を返す

    """
    try:
        group = db.query(GroupsTable).\
            options(joinedload(GroupsTable.profiles)).\
                filter(GroupsTable.id == group_id).\
                    first()        
        return group
    except Exception as e:
        print(e)
        raise e

def get_profiles(group_id:str,db:Session):
    """
    選択したグループに参加しているユーザーのプロフィールを
    返す
    """
    try:
        query = f"""
            SELECT 
                profiles.*, 
                rates.rate4, 
                rates.rate3, 
                rates.rank_id, 
                ranks.rank_name, 
                ranks.point, 
                ranks.init_point,
                ranks.pre_rank_id,
                ranks.next_rank_id
            FROM profiles
            JOIN rates ON rates.profile_id = profiles.id
            JOIN ranks ON rates.rank_id = ranks.id
            WHERE profiles.group = '{group_id}'
            ORDER BY rates.rate4 ASC;
        """    
        result = db.execute(query)
        profiles = []
        for res in result:
            profiles.append(dict(res))
        return profiles
        # profiles = db.query(ProfileTable).\
        #     options(joinedload(ProfileTable.rate)).\
        #         filter(ProfileTable.group == group_id).\
        #             all() 
        return profiles
    except Exception as e:
        print(e)
        raise e

def update_group(group_id: str, update_info:GroupInfoUpdate, path:str, db: Session) -> User:
    """
    ユーザーのデータを更新する
    """
    try:
        group_table = get_selected_group(group_id, db)
        if update_info.title is not None:
            group_table.title = update_info.title
        if update_info.text is not None:
            group_table.text = update_info.text
        if update_info.password is not None:
            group_table.password = update_info.password
        if path is not None:
            group_table.image = path
        db.commit()
        return group_table
    except Exception as e:
            raise e
### DELETE ###
def leave_group(group_id:UUID,user_id:UUID,db:Session)->UUID:
    """
    ユーザーをグループから離脱させる
    """
    try:
        target_group = get_group_by_id(group_id,db)
        if target_group:
            # 既に参加しているかどうかチェック
            profile = get_profile_by_user_and_group(user_id,target_group.id,db)
            if profile is not None:
                if profile.is_active:
                    # 既に参加している場合、非アクティブに
                    res = dis_activate_profile(profile,db)
                    return target_group.id
                else:
                    # 既に非アクティブ 
                    raise ApiException(
                        status_code=status.HTTP_400_BAD_REQUEST,
                        status="fail",
                        detail="this user has already leaved this group",
                    )
            else:
                raise ApiException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    status="fail",
                    detail="this user doesn't join this group",
                )
        else:
            raise ApiException(
                status_code=status.HTTP_400_BAD_REQUEST,
                status="fail",
                detail="Group does not exist",
            )

    except ApiException as e:
        raise e
    
    except Exception as e:
            raise e