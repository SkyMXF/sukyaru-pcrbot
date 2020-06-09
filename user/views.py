from django.shortcuts import render, redirect
from django.http import HttpResponse

from . import models

# Create your views here.
def userinfo(request):
    return render(request, 'user/userinfo.html')

def login(request):

    if request.method == "POST":
        userqq = request.POST.get('userqq')
        password = request.POST.get('password')
        if userqq.strip() and password:     # qq和密码不为空
            # 验证输入qq为数字
            try:
                userqq = int(userqq)
            except:
                message = "输入QQ号格式错误"
                return render(request, "user/login.html", {"message": message})

            # 查询数据库
            try:
                user = models.UserInfo.objects.get(user_qq_id=userqq)
            except:
                message = "没有此QQ记录，请联系公会管理人员添加"
                return render(request, 'user/login.html', {"message": message})
            
            if user.password == password:
                return redirect("/")
            else:
                message = "密码不正确，如果忘记可私聊发送'重置密码'进行重置"
                return render(request, 'user/login.html', {"message": message})

        else:
            message = "QQ或密码不能为空"
            return render(request, "user/login.html", {"message": message})

    return render(request, 'user/login.html')

def setpwd(request):
    return render(request, 'user/setpwd.html')

def logout(request):
    return redirect("/login/")