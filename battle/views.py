from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.utils.timezone import get_default_timezone

import datetime

from . import models
from . import forms

# Create your views here.
def mybattle(request):
    if not request.session.get('is_login', None):
        # 未登录
        return redirect('/user/login')

    # 报刀表单相关
    now_page_qq = request.session.get('userqq', None)
    battle_record_form = forms.BattleRecordForm()
    self_page = True
    
    # 获取出刀记录
    user_battle_record_list_by_day = []         # 每个列表元素为一天的记录
    battle_date_list = []                       # 每个列表元素为一个日期
    battle_dates = models.BattleDate.objects.order_by("battle_date")
    user_all_battle_record = models.NowBattleRecord.objects.filter(user_info__user_qq_id=now_page_qq)
    for now_battle_date in battle_dates:
        # 记录日期
        battle_date_list.append("%d月%d日"%(now_battle_date.battle_date.month, now_battle_date.battle_date.day))

        # 构建当日出刀信息list
        user_now_date_battle_record_list = []
        user_now_date_battle_records = user_all_battle_record.filter(
            record_date__gte=datetime.datetime(
                now_battle_date.battle_date.year, 
                now_battle_date.battle_date.month, 
                now_battle_date.battle_date.day,
                5, 0, 0, 0,     #早上5:00
                tzinfo=get_default_timezone()
            ),
            record_date__lt=datetime.datetime(
                now_battle_date.battle_date+datetime.timedelta(days=1).year, 
                now_battle_date.battle_date+datetime.timedelta(days=1).month, 
                now_battle_date.battle_date+datetime.timedelta(days=1).day,
                5, 0, 0, 0,     #次日早上5:00
                tzinfo=get_default_timezone()
            )
        ).order_by("record_date")
        for now_date_record in user_now_date_battle_records:
            user_now_date_battle_record_list.append({
                "record_time": str(now_date_record.record_date.astimezone(get_default_timezone()).hour) + ":" + str(now_date_record.record_date.minute) + ":" + str(now_date_record.record_date.second),
                "boss_info": str(now_date_record.boss_stage) + "-" + str(now_date_record.boss_id),
                "damage": now_date_record.damage,
                "final_kill": "√" if now_date_record.final_kill else "×",
                "comp_flag": "√" if now_date_record.comp_flag else "×"
            })
        user_battle_record_list_by_day.append(user_now_date_battle_record_list)
    
    now_day_id = 3

    return render(
        request, 'battle/mybattle.html',
        {
            "self_page": self_page,
            "battle_record_form": battle_record_form,
            "user_battle_record": user_battle_record_list_by_day,
            "battle_date_list": battle_date_list,
            "now_day_id": now_day_id
        }
    )

def guildbattle(request):
    if not request.session.get('is_login', None):
        # 未登录
        return redirect('/user/login')

    return render(request, 'battle/guildbattle.html')