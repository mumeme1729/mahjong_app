
from typing import List
from services.cruds.rank_crud import get_rank_by_rankid
from schemas.profile import ProfileBasicSchema
from services.cruds.profile_crud import update_profile_rate
from models.profiles import ProfileTable
from schemas.game import GameCreate
from sqlalchemy.orm.session import Session
from utils.uma import get_uma

def calc_rate_4(game_data: GameCreate, profiles: List[ProfileBasicSchema], db: Session):
    """
    4人麻雀時のレートを計算する
    """

    profile_dict = {str(profile.id): profile for profile in profiles}

    for result in game_data.game_results:
        profile = profile_dict.get(result.profile)
        if not profile:
            continue

        current_rank_info = get_rank_by_rankid(profile.rank_id, db)
        current_rate4 = profile.rate4

        # レートを計算
        uma_value = get_uma(current_rank_info.id, result.rank)
        score = result.score + uma_value
        new_rate4 = current_rate4 + score

        if new_rate4 < 0 and current_rank_info.pre_rank_id != -1:
            # ランクダウン
            new_rank_info = get_rank_by_rankid(current_rank_info.pre_rank_id, db)
            new_rank_id = new_rank_info.id
            new_point =  new_rank_info.init_point
        elif new_rate4 >= current_rank_info.point:
            # ランクアップ
            new_rank_info = get_rank_by_rankid(current_rank_info.next_rank_id, db)
            new_rank_id = new_rank_info.id
            new_point =  new_rank_info.init_point
        elif new_rate4 < 0 and current_rank_info.pre_rank_id == -1:
            # 初心の場合現状維持
            new_rank_id = current_rank_info.id
            new_point =  0
        else:
            # ランクに変動なし
            new_rank_id = current_rank_info.id
            new_point = new_rate4

        try:
            
            update_profile_rate(profile.id, new_rank_id, new_point, db)
        except Exception as e:
            raise Exception(f"Error when updating profile {profile.id}: {str(e)}")


                

def calc_rate_3(game_data:GameCreate, profiles:List[ProfileTable], db:Session):
    """
    3麻雀時のレートを計算する
    """
    
    # 参加者全員のレート合計から平均値を算出する
    total_rate = 0
    for profile in profiles:
        total_rate += profile.rate3
    # 同卓者のレートの平均値
    average_rate = round(total_rate/3)
    #レート更新
    results = game_data.game_results
    for result in results:
        for profile in profiles:
            # プロフィールが一致するもの
            if result.profile == profile.id:
                if result.rank == 1:
                    profile.rate3 = round(profile.rate3+(50+((average_rate - profile.rate3)/70)*0.2))
                elif result.rank == 2:
                    profile.rate3 = round(profile.rate3+(10+((average_rate - profile.rate3)/70)*0.2))
                else:
                    profile.rate3 = round(profile.rate3+(-50+((average_rate - profile.rate3)/70)*0.2))
    # 結果をコミットする
    update_profile_rate(db)
