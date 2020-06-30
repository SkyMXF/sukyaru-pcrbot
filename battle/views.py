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

    # 处理报刀
    if request.method == "POST":
        # 只有自己的页面才可以报刀，所以不存在查询其他qq出刀记录的情况
        post_battle_record_form = forms.BattleRecordForm(request.POST)
        if post_battle_record_form.is_valid():
            post_record_dict = {
                "user_qq": query_qq,
                "boss_real_stage": post_battle_record_form.cleaned_data.get("boss_stage"),
                "boss_id": post_battle_record_form.cleaned_data.get("boss_id"),
                "damage": post_battle_record_form.cleaned_data.get("damage"),
                "record_date": post_battle_record_form.cleaned_data.get("record_date"),
                "final_kill": post_battle_record_form.cleaned_data.get("final_kill"),
                "comp_flag": post_battle_record_form.cleaned_data.get("comp_flag")
            }
            try:
                utils.upload_battle_record(post_record_dict)
            except ValueError as e:
                message = str(e)
                show_dict["message"] = message
                show_dict["battle_record_form"] = post_battle_record_form
        else:
            message = "报刀信息填写格式有误噢..."
            show_dict["message"] = message
            show_dict["battle_record_form"] = post_battle_record_form
    

    if request.method == "GET":
        # 撤销报刀记录
        redo_record_id = request.GET.get("redoreid", None)
        if redo_record_id:
            redo_record_id = int(redo_record_id)
            try:
                utils.redo_battle_record(redo_record_id, operator_qq=request.session['userqq'])
            except ValueError as e:
                message = str(e)
                show_dict["message"] = message

        # 查询他人记录
        get_query_qq = request.GET.get("queryqq", None)
        if get_query_qq:
            query_qq = int(get_query_qq)
            if query_qq != request.session["userqq"]:
                show_dict["self_page"] = False
    
    # 查询个人出刀记录
    show_dict.update(get_user_record_dict(now_page_qq=query_qq))

    show_dict["queryqq"] = query_qq

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
    user_set = UserInfo.objects.filter(active_guild_member=True).order_by("user_auth")

    # 统计整个公会战期间数据
    user_battle_stat_list = []
    user_battle_stat_index_dict = {}
    temp_index = 0
    for now_user_info in user_set:
        user_battle_stat_list.append(
            {
                "user_name": now_user_info.nickname,
                "user_qq": now_user_info.user_qq_id,
                "total_report_num": 0,
                "difficult_report_num": 0,
                "max_report_num": 0,
                "total_damage": 0,
                "total_score": 0,
            }
        )
        user_battle_stat_index_dict["%d"%(now_user_info.user_qq_id)] = temp_index
        temp_index += 1

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

            # 累加全期统计数据
            temp_index = user_battle_stat_index_dict["%d"%(now_user_info.user_qq_id)]

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
                "score": 0
            }
            battle_counter = -1      # 现在计算第x刀及补偿刀
            score = 0.0
            for now_user_date_battle_record in now_user_date_battle_record_set:
                
                # 全期统计数据
                user_battle_stat_list[temp_index]["total_report_num"] += 1
                if now_user_date_battle_record.boss_info.high_difficulty:
                    user_battle_stat_list[temp_index]["difficult_report_num"] += 1
                user_battle_stat_list[temp_index]["total_damage"] += now_user_date_battle_record.damage

                # 当日数据
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

            # 累加全期统计数据
            user_battle_stat_list[temp_index]["max_report_num"] += 3
            user_battle_stat_list[temp_index]["total_score"] += int(score)
        
        # 该页加入总list
        battle_record_list_by_day.append(now_date_battle_record_list)
    
    if now_day_id > len(battle_date_list):  # 访问时间已过公会战期间
        now_day_id = 1

    # 计算总记录中积分/伤害倍率
    for user_stat_dict in user_battle_stat_list:
        if user_stat_dict["total_damage"] > 0:
            user_stat_dict["score_fac"] = "%.2f"%(user_stat_dict["total_score"] / user_stat_dict["total_damage"])
        else:
            user_stat_dict["score_fac"] = "0.0"

    show_dict = {
        "battle_date_list": battle_date_list,
        "battle_record_list_by_day": battle_record_list_by_day,
        "now_day_id": now_day_id,
        "user_battle_stat_list": user_battle_stat_list
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