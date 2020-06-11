from django.shortcuts import render, redirect
from django.http import HttpResponse
from . import forms

from . import models

# Create your views here.
def userinfo(request):
    if not request.session.get('is_login', None):
        # 未登录
        return redirect('/user/login')

    return render(request, 'user/userinfo.html')

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
                message = "输入QQ号格式错误"
                return render(request, "user/login.html", {"message": message, "login_form": login_form})

            # 查询数据库
            try:
                user = models.UserInfo.objects.get(user_qq_id=userqq)
            except:
                message = "没有此QQ记录，请联系公会管理人员添加"
                return render(request, 'user/login.html', {"message": message, "login_form": login_form})
            
            if user.password == password:
                request.session['is_login'] = True
                request.session['userqq'] = user.user_qq_id
                request.session['user_name'] = user.nickname
                user_auth_str = "Unknown"
                if user.user_auth == 0:
                    user_auth_str = "会长"
                elif user.user_auth == 1:
                    user_auth_str = "管理员"
                elif user.user_auth == 2:
                    user_auth_str = "普通群员"
                request.session['user_auth'] = user_auth_str
                return redirect("/user")
            else:
                message = "密码不正确，如果忘记可私聊发送'重置密码'进行重置"
                return render(request, 'user/login.html', {"message": message, "login_form": login_form})

        else:
            message = "QQ或密码输入格式错误"
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
                message = "两次输入的密码不一致"
                return render(request, 'user/setpwd.html', {"message": message})
            
            # 修改数据库    
            userqq = request.session['userqq']
            try:
                userinfo = models.UserInfo.objects.get(user_qq_id=userqq)
            except:
                message = "Unknown ERROR: No record for this qq."
                return render(request, 'user/setpwd.html', {"message": message})
            userinfo.password = password
            userinfo.save()
                
            return redirect("/user/logout")

        else:
            message = "密码输入格式错误"
            return render(request, "user/setpwd.html", {"message": message})

    setpwd_form = forms.SetPasswordForm()
    return render(request, 'user/setpwd.html', {"setpwd_form": setpwd_form})

def logout(request):
    if not request.session.get('is_login', None):
        # 未登录
        return redirect("/user/login")
    request.session.flush()
    return redirect("/user/login")