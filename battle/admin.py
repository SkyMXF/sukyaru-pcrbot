from django.contrib import admin
from .models import BossStatus, BossInfo, NowBattleRecord, LastBattleRecord, BattleDate

# Register your models here.
admin.site.register(BossStatus)
admin.site.register(BossInfo)
admin.site.register(NowBattleRecord)
admin.site.register(LastBattleRecord)
admin.site.register(BattleDate)