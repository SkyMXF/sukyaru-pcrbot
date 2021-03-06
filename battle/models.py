from django.db import models
from user.models import UserInfo

# Create your models here.
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
        return "%s(%d-%d), %d, %.1f, 高难度:%s"%(self.boss_name, self.boss_stage, self.boss_id, self.total_health, self.score_fac, self.high_difficulty)

class BossStatus(models.Model):
    # Boss状态
    boss_info = models.ForeignKey(BossInfo, on_delete=models.CASCADE)
    boss_real_stage = models.IntegerField()       # 真实周目数
    #boss_stage = models.IntegerField()       # 周目数
    #boss_id = models.IntegerField()     # boss编号
    health = models.IntegerField()      # 当前生命值
    now_battle = models.BooleanField(default=False)  # 当前正在作战     # 弃用
    killed = models.BooleanField(default=False)      # 已击杀           # 弃用
    
    def __str__(self):
        return "%s(%d-%d), %d"%(self.boss_info.boss_name, self.boss_real_stage, self.boss_info.boss_id, self.health)

class BattleDate(models.Model):
    # 当前公会战举行日期列表
    battle_date = models.DateField(unique=True)

    def __str__(self):
        return str(self.battle_date)

class NowBattleRecord(models.Model):
    # 当前公会战报刀记录
    record_date = models.DateTimeField()
    user_info = models.ForeignKey(UserInfo, on_delete=models.CASCADE)
    boss_info = models.ForeignKey(BossInfo, on_delete=models.CASCADE)
    boss_real_stage = models.IntegerField()       # 真实周目数
    #boss_stage = models.IntegerField()       # 周目数
    #boss_id = models.IntegerField()     # boss编号
    damage = models.IntegerField()      # 造成伤害
    final_kill = models.BooleanField(default=False)  # 尾刀标记
    comp_flag = models.BooleanField(default=False)  # 补偿刀标记

    def __str__(self):
        return "id_%d, %s, %s, %s(%d-%d), %d"%(self.id, self.user_info.nickname, str(self.record_date), self.boss_info.boss_name, self.boss_real_stage, self.boss_info.boss_id, self.damage)

class NowBattleBoss(models.Model):
    # 设置当前作战boss记录
    now_boss = models.ForeignKey(BossStatus, on_delete=models.CASCADE)
    set_date = models.DateTimeField(auto_now=True)

    def __str__(self):
        return "id_%d, %s, %s"%(self.id, str(self.now_boss), str(self.set_date))