from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.utils.timezone import get_default_timezone

import datetime

from . import models
from . import forms
from main import utils
from user.models import UserInfo

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
        if now_datetime.tz_datetime() >= now_battle_pcr_date.day_end():
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
                "score": int(now_date_record.boss_info.score_fac * now_date_record.damage),
                "final_kill": "√" if now_date_record.final_kill else "×",
                "comp_flag": "√" if now_date_record.comp_flag else "×"
            })
        user_battle_record_list_by_day.append(user_now_date_battle_record_list)
    
    if now_day_id > len(battle_date_list):  # 访问时间已过公会战期间
        now_day_id = 1

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
    
    # 获取出刀记录
    now_datetime = utils.PCRDate(datetime.datetime.utcnow(), tzinfo=get_default_timezone())
    now_day_id = 1
    battle_record_list_by_day = []         # 每个列表元素为一天的记录
    battle_date_list = []                       # 每个列表元素为一个日期
    battle_dates = models.BattleDate.objects.order_by("battle_date")
    all_battle_record = models.NowBattleRecord.objects.all()
    user_set = UserInfo.objects.all().order_by("user_auth")
    # 按日期分表
    for now_battle_date in battle_dates:
        now_battle_pcr_date = utils.PCRDate(now_battle_date.battle_date, tzinfo=get_default_timezone())
        if now_datetime.tz_datetime() >= now_battle_pcr_date.day_end():
            now_day_id += 1

        # 记录日期
        battle_date_list.append("%d月%d日"%(now_battle_pcr_date().month, now_battle_pcr_date().day))

        # 获取当日所有记录
        now_date_battle_record_set = all_battle_record.filter(
            record_date__gte=now_battle_pcr_date.day_begin(),
            record_date__lt=now_battle_pcr_date.day_end()
        )

        # 按user分行
        now_date_battle_record_list = []
        for now_user_info in user_set:
            now_user_date_battle_record_set = now_date_battle_record_set.filter(
                user_info=now_user_info
            ).order_by("record_date")
            row_dict = {
                "user_name": now_user_info.nickname,
                "damage_0": "",
                "comp_0": "",       # 补偿刀
                "damage_1": "",
                "comp_1": "",
                "damage_2": "",
                "comp_2": "",
                "SL": "×",
                "score": "" 
            }
            battle_counter = -1      # 现在计算第x刀及补偿刀
            score = 0.0
            for now_user_date_battle_record in now_user_date_battle_record_set:
                record_type = "comp"    # 补偿刀
                if not now_user_date_battle_record.comp_flag:
                    # 非补偿刀时下标+1
                    battle_counter += 1
                    record_type = "damage"

                if battle_counter < 0: continue     # TODO: 罕见报刀：今日第一刀是补偿刀，需要计入前一日的最后一刀
                if battle_counter > 2: continue     # 异常：该用户该日正常报刀数>3
                
                row_dict["%s_%d"%(record_type, battle_counter)] = "%s(%d-%d) %d"%(   # 例：牛(2-5) 812345
                    now_user_date_battle_record.boss_info.boss_name,
                    now_user_date_battle_record.boss_real_stage,
                    now_user_date_battle_record.boss_info.boss_id,
                    now_user_date_battle_record.damage
                )
                score += now_user_date_battle_record.boss_info.score_fac * now_user_date_battle_record.damage
            row_dict["score"] = "%d"%(int(score))
            now_date_battle_record_list.append(row_dict)
        
        # 该页加入总list
        battle_record_list_by_day.append(now_date_battle_record_list)
    
    if now_day_id > len(battle_date_list):  # 访问时间已过公会战期间
        now_day_id = 1

    show_dict = {
        "battle_date_list": battle_date_list,
        "battle_record_list_by_day": battle_record_list_by_day,
        "now_day_id": now_day_id
    }

    return render(request, 'battle/guildbattle.html', show_dict)