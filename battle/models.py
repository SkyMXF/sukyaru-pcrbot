from django.db import models
from user.models import UserInfo

# Create your models here.
class BossStatus(models.Model):
    # Boss状态
    boss_stage = models.IntegerField()       # 周目数
    boss_id = models.IntegerField()     # boss编号
    health = models.IntegerField()      # 当前生命值
    now_battle = models.BooleanField(default=False)  # 当前正在作战
    killed = models.BooleanField(default=False)     # 已击杀
    
    def __str__(self):
        return "%d-%d"%(self.boss_stage, self.boss_id)

class BossInfo(models.Model):
    # Boss信息
    boss_stage = models.IntegerField()  # 周目数(与属性、倍率对应)
    boss_id = models.IntegerField()     # boss编号
    boss_name = models.CharField(max_length=30)    # boss名
    total_health = models.IntegerField()     # 总血量
    score_fac = models.FloatField(default=1.0)  # 计分倍率
    high_difficulty = models.BooleanField(default=False)    # 高难度boss标记
    detail = models.CharField(max_length=2000)   # 其他文字介绍

    def __str__(self):
        return "%s(%d-%d)"%(self.boss_name, self.boss_stage, self.boss_id)

class NowBattleRecord(models.Model):
    # 当前公会战报刀记录
    record_id = models.IntegerField(unique=True)  # 记录id(用于撤销)
    record_date = models.DateTimeField(auto_now=True)
    user_info = models.ForeignKey(UserInfo, on_delete=models.CASCADE)
    boss_stage = models.IntegerField()       # 周目数
    boss_id = models.IntegerField()     # boss编号
    damage = models.IntegerField()      # 造成伤害
    final_kill = models.BooleanField(default=False)  # 尾刀标记
    comp_flag = models.BooleanField(default=False)  # 补偿刀标记

    def __str__(self):
        return "id_%d, %d-%d, %d"%(self.record_id, self.boss_stage, self.boss_id, self.damage)

class LastBattleRecord(models.Model):
    # 上次公会战报刀记录
    record_id = models.IntegerField(unique=True)  # 记录id(用于撤销)
    record_date = models.DateTimeField()
    user_info = models.ForeignKey(UserInfo, on_delete=models.CASCADE)
    boss_stage = models.IntegerField()       # 周目数
    boss_id = models.IntegerField()     # boss编号
    damage = models.IntegerField()      # 造成伤害
    final_kill = models.BooleanField(default=False)  # 尾刀标记
    comp_flag = models.BooleanField(default=False)  # 补偿刀标记

    def __str__(self):
        return "id_%d, %d-%d, %d"%(self.record_id, self.boss_stage, self.boss_id, self.damage)