from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.utils.timezone import get_default_timezone
from django.db import transaction

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
    
    # 默认查询当前用户报刀记录
    query_qq = request.session.get('userqq', None)

    # 报刀表单相关
    battle_record_form = forms.BattleRecordForm()
    
    # 输出相关
    show_dict = {
        "self_page": True,
        "battle_record_form": battle_record_form
    }

    if request.method == "GET":
        # 撤销报刀记录
        redo_record_id = request.GET.get("redoreid", None)
        if not (redo_record_id is None):
            redo_record_id = int(redo_record_id)
            try:
                now_record = models.NowBattleRecord.objects.get(id=redo_record_id)
            except: # 没有改id记录
                message = "出错了...凯露酱这里没有这条需要撤销的记录诶"
                show_dict["message"] = message
                return render(
                    request, 'battle/mybattle.html', show_dict
                )
            # 检查权限
            if request.session['userqq'] == now_record.user_info.user_qq_id or request.session['user_auth'] < 2:    # 本人删除或管理员删除
                try:
                    utils.boss_status_redo(now_record)
                except:
                    message = "重置BOSS状态时出现问题~"
                    show_dict["message"] = message
                try:
                    now_record.delete()
                except:
                    message = "删除记录时出现了错误~该记录可能已经被清除了"
                    show_dict["message"] = message
            else:
                message = "骑士君没有删除这条记录的权限噢~"
                show_dict["message"] = message
                return render(
                    request, 'battle/mybattle.html', show_dict
                )

        # 查询他人记录
        query_qq = int(request.GET.get("queryqq", None))
        if not (query_qq is None):
            query_qq = int(query_qq)
            if query_qq != request.session["userqq"]:
                show_dict["self_page"] = False
    
    # 查询个人出刀记录
    show_dict.update(get_user_record_dict(now_page_qq=query_qq))

    return render(
        request, 'battle/mybattle.html', show_dict
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
                "user_qq": now_user_info.user_qq_id,
                "damage_0": "",
                "comp_0": "",       # 补偿刀
                "damage_1": "",
                "comp_1": "",
                "damage_2": "",
                "comp_2": "",
                "SL": "×",
                "score": 0
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
            row_dict["score"] = int(score)
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

def get_user_record_dict(now_page_qq):
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
                "record_id": now_date_record.id,
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
    
    show_dict = {
        "user_battle_record": user_battle_record_list_by_day,
        "battle_date_list": battle_date_list,
        "now_day_id": now_day_id
    }

    return show_dict