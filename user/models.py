from django.db import models

# Create your models here.
class UserInfo(models.Model):
    user_qq_id = models.BigIntegerField(unique=True)
    password = models.CharField(max_length=20)
    nickname = models.CharField(max_length=30)
    user_type = models.IntegerField(default=2)  # 0-会长, 1-管理员, 2-普通群员

    def __str__(self):
        user_type_str = "Unknown"
        if self.user_type == 0:
            user_type_str = "会长"
        elif self.user_type == 1:
            user_type_str = "管理员"
        elif self.user_type == 2:
            user_type_str = "普通群员"

        return "qq: %s, pwd: %s, name: %s, type: %s"%(str(self.user_qq_id), str(self.password), str(self.nickname), user_type_str)