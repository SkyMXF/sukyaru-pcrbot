from django.contrib import admin
from .models import BossStatus, BossInfo, NowBattleRecord, BattleDate, NowBattleBoss

# Register your models here.
admin.site.register(BossStatus)
admin.site.register(BossInfo)
admin.site.register(NowBattleRecord)
admin.site.register(BattleDate)
admin.site.register(NowBattleBoss)