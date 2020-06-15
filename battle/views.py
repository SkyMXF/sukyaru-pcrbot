from django.shortcuts import render, redirect
from django.http import HttpResponse

from . import models
from . import forms

# Create your views here.
def mybattle(request):
    if not request.session.get('is_login', None):
        # 未登录
        return redirect('/user/login')

    now_page_qq = request.session.get('userqq', None)
    battle_record_form = forms.BattleRecordForm()
    self_page = True
    return render(request, 'battle/mybattle.html', {"self_page": self_page, "battle_record_form": battle_record_form})

def guildbattle(request):
    if not request.session.get('is_login', None):
        # 未登录
        return redirect('/user/login')

    return render(request, 'battle/guildbattle.html')