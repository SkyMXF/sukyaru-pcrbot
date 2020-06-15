from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.utils.timezone import get_default_timezone

import datetime

from . import models
from . import forms
from main import utils

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
    now_datetime = utils.PCRDate(datetime.datetime.utcnow(), tzinfo=get_default_timezone())
    now_day_id = 1
    user_battle_record_list_by_day = []         # 每个列表元素为一天的记录
    battle_date_list = []                       # 每个列表元素为一个日期
    battle_dates = models.BattleDate.objects.order_by("battle_date")
    user_all_battle_record = models.NowBattleRecord.objects.filter(user_info__user_qq_id=now_page_qq)
    for now_battle_date in battle_dates:
        now_battle_pcr_date = utils.PCRDate(now_battle_date.battle_date, tzinfo=get_default_timezone())
        if now_datetime() < now_battle_pcr_date.day_begin():
            now_day_id += 1

        # 记录日期
        battle_date_list.append("%d月%d日"%(now_battle_pcr_date().month, now_battle_pcr_date().day))

        # 构建当日出刀信息list
        user_now_date_battle_record_list = []
        user_now_date_battle_records = user_all_battle_record.filter(
            record_date__gte=now_battle_pcr_date.day_begin(),
            record_date__lt=now_battle_pcr_date.day_end()
        ).order_by("record_date")
        for now_date_record in user_now_date_battle_records:
            record_pcr_date = utils.PCRDate(now_date_record.record_date, tzinfo=get_default_timezone())
            user_now_date_battle_record_list.append({
                "record_time": record_pcr_date.tz_datetime().strftime("%m-%d %H:%M:%S"),
                "boss_info": "%s(%d-%d)"%(now_date_record.boss_info.boss_name, now_date_record.boss_real_stage, now_date_record.boss_info.boss_id),
                "damage": now_date_record.damage,
                "final_kill": "√" if now_date_record.final_kill else "×",
                "comp_flag": "√" if now_date_record.comp_flag else "×"
            })
        user_battle_record_list_by_day.append(user_now_date_battle_record_list)

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