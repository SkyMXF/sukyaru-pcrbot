from django.db import models
from user.models import UserInfo

# Create your models here.
class Title(models.Model):
    title_prefix = models.CharField(max_length=30)  # 称号前缀（如：第X期，在部分页面不显示）
    title_name = models.CharField(max_length=30)    # 称号名称
    good_worker = models.BooleanField(default=False)    # 是否上优秀员工墙
    
    def __str__(self):
        return "[%s]%s, 优秀：%s"%(self.title_prefix, self.title_name, str(self.good_worker))

class UserTitle(models.Model):
    user_info = models.ForeignKey(UserInfo, on_delete=models.CASCADE)
    award_date = models.DateTimeField(auto_now=True)
    title = models.ForeignKey(Title, on_delete=models.CASCADE)
    record_num = models.IntegerField()
    record_str = models.CharField(max_length=50)
    
    def __str__(self):
        return "[%s]%s, %s"%(str(self.award_date), self.user_info.nickname, self.title)

class Announcement(models.Model):
    anno_detail = models.CharField(max_length=1000)
    anno_date = models.DateTimeField(auto_now=True)

    def __str__(self):
        return "[%s]%s"%(str(self.anno_date), self.anno_detail)