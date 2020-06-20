import hashlib
import datetime

from django.db import transaction
from django.utils.timezone import get_default_timezone

from battle.models import NowBattleRecord, BattleDate, BossInfo, BossStatus, NowBattleBoss
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

def boss_status_promote(record_dict, record_boss_info):
    # 根据报刀信息，更新boss状态
    # 返回： 0-普通，1-报刀boss被击杀，2-新boss报刀，疑似前一boss被击杀

    # 尝试获取对应boss状态
    boss_status_set = BossStatus.objects.filter(boss_real_stage=record_dict["boss_real_stage"], boss_info__boss_id=record_dict["boss_id"])
    find_boss = None
    if len(boss_status_set) <= 0:
        find_boss = None
    else:
        find_boss = boss_status_set.first()
    
    # 新boss创建信息
    if find_boss is None:
        find_boss = BossStatus.objects.create(
            boss_info_id=record_boss_info.id,
            boss_real_stage=record_dict["boss_real_stage"],
            health=record_boss_info.total_health - record_dict["damage"],
            now_battle=False,
            killed=False
        )
        NowBattleBoss.objects.create(now_boss=find_boss)    # 更新当前作战boss
        return 2    # 新boss报刀，疑似前一boss被击杀
    # 更新血量
    else:
        find_boss.health = find_boss.health - record_dict["damage"]
        find_boss.save()

    if find_boss.health <= 0:
        # 报刀boss被击杀
        return 1
    else:
        return 0    # 一般返回
        

def boss_status_redo(battle_record):
    # 撤销报刀时更新boss状态

    # 获取对应boss状态
    boss_status_set = BossStatus.objects.filter(boss_real_stage=battle_record.boss_real_stage, boss_info__boss_id=battle_record.boss_info.boss_id)
    if len(boss_status_set) <= 0:
        raise ValueError("异常：撤销报刀时发生错误，不存在报刀记录对应的boss信息")
    
    now_boss_status = boss_status_set.first()
    now_boss_status.health = now_boss_status.health + battle_record.damage
    now_boss_status.save()

    # 检查报刀记录，如果只有待撤销的记录指向该boss_status，则更新NowBattleBoss表
    # TODO: 修正错误报刀，更新NowBattleBoss表

def upload_battle_record(record_dict):
    # 公用函数：向数据库上传报刀记录
    # 会调用boss_status_promote更新boss status
    # 会检查该日是否已满3刀
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
        raise ValueError("报刀失败：骑士君填写的日期不在公会战日期内噢")

    # 获取user的数据库id
    try:
        user_info = UserInfo.objects.get(user_qq_id=record_dict["user_qq"])
    except:
        raise ValueError("报刀失败：凯露酱这里没有这位骑士君的qq记录噢")

    if not user_info.active_guild_member:
        raise ValueError("报刀失败：公会成员'%s'不是当期公会战成员中噢，请联系管理员设置"%(user_info.nickname))
    
    # 获取boss信息
    boss_info_set = BossInfo.objects.filter(boss_id=record_dict["boss_id"])
    min_d = 1000
    record_boss_info = None
    for boss_info in boss_info_set:
        if min_d > abs(record_dict["boss_real_stage"] - boss_info.boss_stage):
            record_boss_info = boss_info
            min_d = abs(record_dict["boss_real_stage"] - boss_info.boss_stage)
    if record_boss_info is None:
        raise ValueError("报刀失败：凯露酱这里没有指定boss的信息(%d-%d)，如果骑士君确认输入无误，请联系管理员添加噢"%(
        record_dict["boss_real_stage"], record_dict["boss_id"])
    )

    try:
        with transaction.atomic():
            # 检查是否已满3刀
            user_today_battle_record_set = NowBattleRecord.objects.filter(
                user_info__user_qq_id=record_dict["user_qq"],
                record_date__gte=record_date.day_begin(),
                record_date__lt=record_date.day_end(),
            ).order_by("record_date")
            if len(user_today_battle_record_set) > 0:
                if user_today_battle_record_set.last().comp_flag and record_dict["comp_flag"]:
                    raise ValueError("报刀失败：最近的一次报告也是补偿刀，不可以连续报告补偿刀噢")
            elif record_dict["comp_flag"]:
                raise ValueError("报刀失败：每日第一刀不可以记为补偿刀噢，如果确实需要报告前一日的补偿刀，可以在公会网站中手动报刀，时间选择为前一日最后一刀之后")
            
            user_today_battle_record_set = user_today_battle_record_set.filter(comp_flag=False)
            if len(user_today_battle_record_set) >= 3 and record_dict["comp_flag"] == False:
                raise ValueError("报刀失败：骑士君这一天已经有3次非补偿刀的报刀了噢")

            # 生成record
            upload_record = NowBattleRecord.objects.create(
                record_date=record_dict["record_date"],
                user_info_id=user_info.id,
                boss_info_id=record_boss_info.id,
                boss_real_stage=record_dict["boss_real_stage"],
                damage=record_dict["damage"],
                final_kill=record_dict["final_kill"],
                comp_flag=record_dict["comp_flag"]
            )
            boss_status_promote(record_dict, record_boss_info)    # 更新公会战总进度
    
    except ValueError as e:
        raise ValueError(str(e))
    except Exception as e:
        print(e)
        raise ValueError("数据提交给凯露酱时发生错误，请重新提交试试，如果依然出现错误，请联系管理员")

    return upload_record

def redo_battle_record(record_id:int, operator_qq:int):
    # 撤销报刀记录
    # 会调用boss_status_redo
    # 输入：record_id: int, 需要删除的记录id。operator_qq: int, 操作者的QQ。
    # 无返回值
    # 异常情况以ValueError形式返回

    # 获取操作者权限
    try:
        operator_info = UserInfo.objects.get(user_qq_id=operator_qq)
    except:
        raise ValueError("撤销失败：凯露酱这里没有操作者的qq的记录")
    
    try:
        with transaction.atomic():
            # 获取报刀记录
            now_record = NowBattleRecord.objects.get(id=record_id)

            # 检查权限
            if operator_qq == now_record.user_info.user_qq_id or operator_info.user_auth < 2:    # 本人删除或管理员删除
                boss_status_redo(now_record)
                now_record.delete()
            else:
                message = "骑士君没有删除这条记录的权限噢~"
                raise ValueError(message)
    except ValueError as e:
        raise ValueError(str(e))
    except Exception as e:
        print(e)
        raise ValueError("撤销时发生错误，可能该记录已被删除了噢~")

def cal_mine(now_best_rank: int):

    return cal_season_diam(now_best_rank), cal_all_season_diam(now_best_rank)

def cal_season_diam(rank):
    
    if rank > 8100:
        return 15 * (rank - 1 - 8100) // 100 + 15 + cal_season_diam(8100)
    if rank > 4000:
        return 50 * (rank - 1 - 4000) // 100 + 50 + cal_season_diam(4000)
    elif rank > 2001:
        return 1 * (rank - 2001) + cal_season_diam(2001)
    elif rank > 1001:
        return 2 * (rank - 1001) + cal_season_diam(1001)
    elif rank > 501:
        return 2 * (rank - 501) + cal_season_diam(501)
    elif rank > 201:
        return 3 * (rank - 201) + cal_season_diam(201)
    elif rank > 101:
        return 5 * (rank - 101) + cal_season_diam(101)
    elif rank > 11:
        return 10 * (rank - 11) + cal_season_diam(11)
    else:
        return 50 * (rank - 1)

def cal_all_season_diam(rank):
    
    if rank > 12000:
        return 45 * (rank - 1 - 12000) // 100 + 80 + cal_all_season_diam(12000)
    elif rank > 8000:
        return 95 * (rank - 1 - 8000) // 100 + 95 + cal_all_season_diam(8000)
    elif rank > 4001:
        return 1 * (rank - 4001) + cal_all_season_diam(4001)
    elif rank > 2001:
        return 3 * (rank - 2001) + cal_all_season_diam(2001)
    elif rank > 1001:
        return 5 * (rank - 1001) + cal_all_season_diam(1001)
    elif rank > 501:
        return 7 * (rank - 501) + cal_all_season_diam(501)
    elif rank > 201:
        return 13 * (rank - 201) + cal_all_season_diam(201)
    elif rank > 101:
        return 35 * (rank - 101) + cal_all_season_diam(101)
    elif rank > 11:
        return 60 * (rank - 11) + cal_all_season_diam(11)
    else:
        return 550 * (rank - 1)