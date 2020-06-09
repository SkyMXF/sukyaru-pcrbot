from django.db import models

# Create your models here.
class UserInfo(models.Model):
    user_qq_id = models.BigIntegerField(unique=True)
    password = models.CharField(max_length=256)

    def __str__(self):
        return "qq: %s, pwd: %s"%(str(self.user_qq_id), str(self.password))

class UserGroup(models.Model):
    # 一个qq可以属于多个群
    user_qq_id = models.ForeignKey(UserInfo, on_delete=models.CASCADE)
    group_id = models.BigIntegerField()
    nickname = models.CharField(max_length=256)
    
    def __str__(self):
        return "qq: %s, group_id: %s, nickname: %s"%(str(self.user_qq_id), str(self.group_id), str(self.nickname))