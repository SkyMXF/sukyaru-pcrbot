from django.db import models

# Create your models here.
class UserInfo(models.Model):
    user_qq_id = models.BigIntegerField()
    qq_group_id = models.BigIntegerField()
    nickname = models.CharField(max_length=30)