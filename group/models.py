from django.db import models

# Create your models here.
class GroupInfo(models.Model):
    group_id = models.BigIntegerField(unique=True)
    group_name = models.CharField(max_length=256)

    def __str__(self):
        return "group_id: %s, name: %s"%(str(self.group_id), str(self.group_name))