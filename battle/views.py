from django.shortcuts import render, redirect
from django.http import HttpResponse

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
    user_battle_record_list_by_day = [] # 每个列表元素为一天的记录
    battle_date_list = models.BattleDate.objects.all()
    for now_battle_date in battle_date_list:
        print(battle_date_list)

    return render(request, 'battle/mybattle.html', {"self_page": self_page, "battle_record_form": battle_record_form})

def guildbattle(request):
    if not request.session.get('is_login', None):
        # 未登录
        return redirect('/user/login')

    return render(request, 'battle/guildbattle.html')