from django.db import models

# Create your models here.
class UserInfo(models.Model):
    user_qq_id = models.BigIntegerField(unique=True)
    password = models.CharField(max_length=128)
    nickname = models.CharField(max_length=30)
    user_auth = models.IntegerField(default=2)  # 0-会长, 1-管理员, 2-普通群员
    user_add_type = models.IntegerField(default=0)  # 该位置现在用来表示SL状态，0-未SL，1-已经SL
    active_guild_member = models.BooleanField(default=True) # 是否为当前公会成员(该项为False的成员不会显示在当期伤害记录中)

    def __str__(self):
        user_auth_str = "Unknown"
        if self.user_auth == 0:
            user_auth_str = "会长"
        elif self.user_auth == 1:
            user_auth_str = "管理员"
        elif self.user_auth == 2:
            user_auth_str = "普通群员"

        return "qq: %s, pwd: %s, name: %s, type: %s"%(str(self.user_qq_id), str(self.password), str(self.nickname), user_auth_str)