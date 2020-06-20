from django.shortcuts import render, redirect
from django.http import HttpResponse

from main import utils

# Create your views here.
def tools(request):
    if not request.session.get('is_login', None):
        # 未登录
        return redirect("/user/login")
    
    if request.method == "GET":
        best_rank = request.GET.get("bestrank", None)
        if best_rank:
            try:
                best_rank = int(best_rank)
            except:
                message = "输入挖矿计算器的排名需要是1-15001范围的数字噢"
                return render(request, 'guild/tools.html', {"message": message})

            season_diam, all_season_diam = utils.cal_mine(best_rank)

            return render(request, 'guild/tools.html', {"season_diam": season_diam, "all_season_diam": all_season_diam})
    
    return render(request, 'guild/tools.html')