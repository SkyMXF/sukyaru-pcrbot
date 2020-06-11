from django.urls import path

from . import views

urlpatterns = [
    path('', views.userinfo, name='userinfo'),
    path('login', views.login, name='login'),
    path('setpwd', views.setpwd, name='set_password'),
    path('logout', views.logout, name='logout')
]