import hashlib
import datetime
from battle.models import NowBattleRecord
from django.db import transaction

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
    # 输入：dict, 包含boss_real_stage, boss_id, damage, record_date, final_kill, comp_flag
    # 无返回值
    # 异常情况以ValueError形式返回

    try:
        with transaction.atomic():
            # 检查是否已满3刀
            

            # 构造record
    
    except:
        raise ValueError("数据提交给凯露酱时发生错误，请重新提交试试，如果依然出现错误，请联系管理员")
