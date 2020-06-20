from user.models import UserInfo
from battle.models import BossStatus
from main import utils

def report(battle_record_dict):

    # 权限检查
    try:
        operator_info = UserInfo.objects.get(user_qq_id=battle_record_dict["operator_qq"])
    except:
        return False, "报刀失败：凯露酱这里没有操作者的qq的记录噢"
    if battle_record_dict["operator_qq"] != battle_record_dict["user_qq"] and operator_info.user_auth >= 2:    # 操作者非本人或管理员
        return False, "报刀失败：骑士君没有代替报刀的权限噢~"

    # 调用utils函数
    try:
        upload_record = utils.upload_battle_record(battle_record_dict)
    except ValueError as e:
        return False, str(e)

    # TODO: 烂代码：获取出刀玩家名称
    try:
        user_info = UserInfo.objects.get(user_qq_id=battle_record_dict["user_qq"])
    except:
        return False, "报刀失败：出现异常错误，请再试一次或联系管理员"

    # TODO: 烂代码：获取boss信息
    try:
        boss_status = BossStatus.objects.get(boss_real_stage=battle_record_dict["boss_real_stage"], boss_info__boss_id=battle_record_dict["boss_id"])
    except:
        return False, "报刀失败：出现异常错误，请再试一次或联系管理员"
    
    return True, "报刀成功：[记录id: %d]%s对BOSS%s(%d-%d)造成了%d点伤害，BOSS当前血量：%d/%d"%(
        upload_record.id,
        user_info.nickname,
        boss_status.boss_info.boss_name,
        battle_record_dict["boss_real_stage"],
        battle_record_dict["boss_id"],
        battle_record_dict["damage"],
        boss_status.health,
        boss_status.boss_info.total_health
    )

def redo(record_id, operator_qq):

    try:
        utils.redo_battle_record(record_id, operator_qq)
    except ValueError as e:
        return False, str(e)
    
    return True, "撤销成功~"