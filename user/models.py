from django.db import models

# Create your models here.
class UserInfo(models.Model):
    user_qq_id = models.BigIntegerField()
    qq_group_id = models.BigIntegerField()
    nickname = models.CharField(max_length=30)

    def __str__(self):
        return "qq: %s, group id: %s, nickname: %s"%(
            self.user_qq_id, self.qq_group_id, self.nickname
        )