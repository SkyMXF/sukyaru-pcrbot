from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.utils.timezone import get_default_timezone

from main import utils
from . import forms
from . import models
from guild.models import UserTitle, Announcement
from battle.models import NowBattleRecord, NowBattleBoss

import datetime

# Create your views here.
def userinfo(request):
    if not request.session.get('is_login', None):
        # 未登录
        return redirect('/user/login')
    
    show_info_dict = {}

    # 查询用户昵称权限信息
    user_qq_id = request.session.get('userqq', None)
    user = models.UserInfo.objects.get(user_qq_id=user_qq_id)
    user_auth_str = "Unknown"
    if user.user_auth == 0:
        user_auth_str = "会长"
    elif user.user_auth == 1:
        user_auth_str = "管理员"
    elif user.user_auth == 2:
        user_auth_str = "普通群员"
    show_info_dict["user_auth_str"] = user_auth_str
    show_info_dict["user_name"] = user.nickname

    # 查询荣誉称号
    user_title_info = UserTitle.objects.filter(user_info_id=user.id).order_by("award_date")
    if len(user_title_info) <= 0:
        show_info_dict["user_title"] = "暂无"
    else:
        show_info_dict["user_title"] = user_title_info.last().title.title_name.name
    
    # 查询出刀次数
    now_datetime = utils.PCRDate(datetime.datetime.utcnow(), tzinfo=get_default_timezone())
    user_today_battle_record_set = NowBattleRecord.objects.filter(
        record_date__gte=now_datetime.day_begin(),
        record_date__lt=now_datetime.day_end(),
        user_info_id=user.id,
        comp_flag=False
    )
    show_info_dict["user_battle_record_count"] = len(user_today_battle_record_set)
    
    # 查询当前boss信息
    now_battle_boss = NowBattleBoss.objects.all().order_by("set_date")
    if len(now_battle_boss) <= 0:
        show_info_dict["now_battle_boss_name"] = "暂无"
        show_info_dict["now_battle_boss_diff"] = "否"
        show_info_dict["now_battle_boss_health"] = "0/0"
    else:
        now_battle_boss = now_battle_boss.last()
        show_info_dict["now_battle_boss_name"] = now_battle_boss.now_boss.boss_info.boss_name
        show_info_dict["now_battle_boss_diff"] = "是" if now_battle_boss.now_boss.boss_info.high_difficulty else "否"
        show_info_dict["now_battle_boss_health"] = "%d/%d"%(now_battle_boss.now_boss.health, now_battle_boss.now_boss.boss_info.total_health)

    # 查询公告
    guild_anno = Announcement.objects.all().order_by("anno_date")
    if len(guild_anno) <= 0:
        show_info_dict["guild_anno"] = "现在没有公告噢"
    else:
        show_info_dict["guild_anno"] = guild_anno.last().anno_detail
    
    # 查询上期高级称号
    MVP_info = UserTitle.objects.filter(title__title_name__tid=0).order_by("award_date")     # 0-MVP
    if len(MVP_info) <= 0:
        show_info_dict["MVP_name"] = "无"
        show_info_dict["MVP_record_num"] = 0
    else:
        show_info_dict["MVP_name"] = MVP_info.last().user_info.nickname
        show_info_dict["MVP_record_num"] = MVP_info.last().record_num
    HighDamage_info = UserTitle.objects.filter(title__title_name__tid=1).order_by("award_date")   # 1-最高输出
    if len(MVP_info) <= 0:
        show_info_dict["HighDamage_name"] = "无"
        show_info_dict["HighDamage_record_num"] = 0
    else:
        show_info_dict["HighDamage_name"] = HighDamage_info.last().user_info.nickname
        show_info_dict["HighDamage_record_num"] = HighDamage_info.last().record_num
    XTS_info = UserTitle.objects.filter(title__title_name__tid=2).order_by("award_date")          # 2-小天使
    if len(XTS_info) <= 0:
        show_info_dict["XTS_name"] = "无"
        show_info_dict["XTS_record_num"] = 0
    else:
        show_info_dict["XTS_name"] = XTS_info.last().user_info.nickname
        show_info_dict["XTS_record_num"] = XTS_info.last().record_num


    return render(request, 'user/userinfo.html', show_info_dict)

def login(request):

    if request.session.get('is_login', None):  # 不允许重复登录
        return redirect('/user')

    if request.method == "POST":
        login_form = forms.UserLoginForm(request.POST)
        if login_form.is_valid():
            userqq = login_form.cleaned_data.get('userqq')
            password = login_form.cleaned_data.get('password')
            # 验证输入qq为数字
            try:
                userqq = int(userqq)
            except:
                message = "输入QQ号格式不对噢0.0"
                return render(request, "user/login.html", {"message": message, "login_form": login_form})

            # 查询数据库
            try:
                user = models.UserInfo.objects.get(user_qq_id=userqq)
            except:
                message = "凯露酱没有此QQ记录0.0，请联系公会管理人员添加噢~"
                return render(request, 'user/login.html', {"message": message, "login_form": login_form})
            
            if user.password == utils.pwd_hash(password):
                request.session['is_login'] = True
                request.session['userqq'] = user.user_qq_id
                request.session['user_name'] = user.nickname
                request.session['user_auth'] = user.user_auth
                return redirect("/user")
            else:
                message = "密码不正确0.0，如果忘记可私聊凯露酱发送'重置密码'进行重置"
                return render(request, 'user/login.html', {"message": message, "login_form": login_form})

        else:
            message = "QQ或密码输入格式错误0.0"
            return render(request, "user/login.html", {"message": message, "login_form": login_form})

    # 直接url访问
    login_form = forms.UserLoginForm()
    return render(request, 'user/login.html', {"login_form": login_form})

def setpwd(request):
    if not request.session.get('is_login', None):
        # 未登录
        return redirect("/user/login")
    
    if request.method == "POST":
        setpwd_form = forms.SetPasswordForm(request.POST)
        if setpwd_form.is_valid():
            password = setpwd_form.cleaned_data.get('password')
            retype_password = setpwd_form.cleaned_data.get('retype_password')

            if password != retype_password:
                message = "两次输入的密码不一样噢0.0"
                return render(request, 'user/setpwd.html', {"message": message, "setpwd_form": setpwd_form})
            
            # 修改数据库    
            userqq = request.session['userqq']
            try:
                userinfo = models.UserInfo.objects.get(user_qq_id=userqq)
            except:
                message = "Unknown ERROR: No record for this qq."
                return render(request, 'user/setpwd.html', {"message": message, "setpwd_form": setpwd_form})
            userinfo.password = utils.pwd_hash(password)
            userinfo.save()
                
            return redirect("/user/logout")

        else:
            message = "密码输入格式错误0.0"
            return render(request, "user/setpwd.html", {"message": message, "setpwd_form": setpwd_form})

    setpwd_form = forms.SetPasswordForm()
    return render(request, 'user/setpwd.html', {"setpwd_form": setpwd_form})

def logout(request):
    if not request.session.get('is_login', None):
        # 未登录
        return redirect("/user/login")
    request.session.flush()
    return redirect("/user/login")
    