import hashlib
import datetime

from django.db import transaction
from django.utils.timezone import get_default_timezone

from battle.models import NowBattleRecord, BattleDate, BossInfo, BossStatus
from user.models import UserInfo

def pwd_hash(s, salt='dfssaltsalt'):# 加点盐
    h = hashlib.sha256()
    s += salt
    h.update(s.encode())  # update方法只接收bytes类型
    return h.hexdigest()

class PCRDate():

    def __init__(self, real_datetime, tzinfo):
        self.real_datetime = real_datetime
        self.tzinfo = tzinfo
    
    def day_begin(self):
        return datetime.datetime(
                self.real_datetime.year, 
                self.real_datetime.month, 
                self.real_datetime.day,
                5, 0, 0, 0,     #当日早上5:00
                tzinfo=self.tzinfo
            )
    
    def day_end(self):
        return datetime.datetime(
                (self.real_datetime+datetime.timedelta(days=1)).year, 
                (self.real_datetime+datetime.timedelta(days=1)).month, 
                (self.real_datetime+datetime.timedelta(days=1)).day,
                5, 0, 0, 0,     #次日早上5:00
                tzinfo=self.tzinfo
            )
    
    def tz_datetime(self):
        return self.real_datetime.astimezone(self.tzinfo)
    
    def __call__(self):
        return self.real_datetime

def boss_status_promote(battle_record):
    pass

def boss_status_redo(battle_record):
    pass

def upload_battle_record(record_dict):
    # 公用函数：向数据库上传报刀记录
    # 会调用boss_status_promote更新boss status
    # 会检查改日是否已满3刀
    # 输入：dict, 包含user_qq, boss_real_stage, boss_id, damage, record_date, final_kill, comp_flag
    # 无返回值
    # 异常情况以ValueError形式返回

    # 日期检查
    record_datetime_pcr = PCRDate(record_dict["record_date"], tzinfo=get_default_timezone())
    battle_date_set = BattleDate.objects.order_by("battle_date")
    record_date = None
    for battle_date in battle_date_set:
        # 确定报刀的pcr日期
        battle_date_pcr = PCRDate(battle_date.battle_date, tzinfo=get_default_timezone())
        if record_datetime_pcr.tz_datetime() >= battle_date_pcr.day_begin() and record_datetime_pcr.tz_datetime() < battle_date_pcr.day_end():
            record_date = battle_date_pcr
            break
    if record_date is None:
        raise ValueError("上传失败：骑士君填写的日期不在公会战日期内噢")

    # 获取user的数据库id
    try:
        user_info = UserInfo.objects.get(user_qq_id=record_dict["user_qq"])
    except:
        raise ValueError("上传失败：凯露酱这里没有这位骑士君的qq记录噢")
    
    # 获取boss信息
    boss_info_set = BossInfo.objects.filter(boss_id=record_dict["boss_id"])
    min_d = 1000
    record_boss_info = None
    for boss_info in boss_info_set:
        if min_d > abs(record_dict["boss_real_stage"] - boss_info.boss_stage):
            record_boss_info = boss_info
            min_d = abs(record_dict["boss_real_stage"] - boss_info.boss_stage)
    if record_boss_info is None:
        raise ValueError("上传失败：凯露酱这里没有指定boss的信息(%d-%d)，如果骑士君确认输入无误，请联系管理员添加噢"%(
        record_dict["boss_real_stage"], record_dict["boss_id"])
    )

    try:
        with transaction.atomic():
            # 检查是否已满3刀
            user_today_battle_record_set = NowBattleRecord.objects.filter(
                user_info__user_qq_id=record_dict["user_qq"],
                record_date__gte=record_date.day_begin(),
                record_date__lt=record_date.day_end(),
                comp_flag=False
            )
            if len(user_today_battle_record_set) >= 3:
                raise ValueError("上传失败：骑士君这一天已经有3次非补偿刀的报刀了噢")

            # 生成record
            NowBattleRecord.objects.create(
                record_date=record_dict["record_date"],
                user_info_id=user_info.id,
                boss_info_id=record_boss_info.id,
                boss_real_stage=record_dict["boss_real_stage"],
                damage=record_dict["damage"],
                final_kill=record_dict["final_kill"],
                comp_flag=record_dict["comp_flag"]
            )
    
    except Exception as e:
        print(e)
        raise ValueError("数据提交给凯露酱时发生错误，请重新提交试试，如果依然出现错误，请联系管理员")
