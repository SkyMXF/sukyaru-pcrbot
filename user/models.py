from django.db import models

# Create your models here.
class UserInfo(models.Model):
    user_qq_id = models.BigIntegerField(unique=True)
    password = models.CharField(max_length=256)
    nickname = models.CharField(max_length=30)
    user_auth = models.IntegerField(default=2)  # 0-会长, 1-管理员, 2-普通群员
    user_add_type = models.IntegerField(default=0)  # 0-自动添加, 1-特殊途径添加(群内不存在的qq)

    def __str__(self):
        user_auth_str = "Unknown"
        if self.user_auth == 0:
            user_auth_str = "会长"
        elif self.user_auth == 1:
            user_auth_str = "管理员"
        elif self.user_auth == 2:
            user_auth_str = "普通群员"

        return "qq: %s, pwd: %s, name: %s, type: %s"%(str(self.user_qq_id), str(self.password), str(self.nickname), user_auth_str)