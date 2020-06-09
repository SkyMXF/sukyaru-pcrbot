from django.shortcuts import render, redirect
from django.http import HttpResponse

# Create your views here.
def userinfo(request):
    return render(request, 'user/userinfo.html')

def login(request):
    return render(request, 'user/login.html')

def setpwd(request):
    return render(request, 'user/setpwd.html')

def logout(request):
    return redirect("/login/")