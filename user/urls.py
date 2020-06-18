from django.urls import path

from . import views

urlpatterns = [
    path('', views.userinfo, name='userinfo'),
    path('login', views.login, name='login'),
    path('setpwd', views.setpwd, name='set_password'),
    path('setname', views.setname, name='set_name'),
    path('logout', views.logout, name='logout')
]