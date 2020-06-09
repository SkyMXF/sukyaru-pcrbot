from django.db import models

# Create your models here.
class UserInfo(models.Model):
    user_qq_id = models.BigIntegerField(unique=True)
    password = models.CharField(max_length=256)

class UserGroup(models.Model):
    # 一个qq可以属于多个群
    user_qq_id = models.ForeignKey(UserInfo, on_delete=models.CASCADE)
    group_id = models.BigIntegerField()
    nickname = models.CharField(max_length=256)