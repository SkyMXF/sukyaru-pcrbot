from django.shortcuts import render, redirect
from django.http import HttpResponse

# Create your views here.
def userinfo(request):
    return render(request, 'userinfo.html')

def login(request):
    return render(request, 'login.html')

def setpwd(request):
    return render(request, 'setpwd.html')

def logout(request):
    return redirect("/login/")