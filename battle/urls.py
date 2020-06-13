from django.urls import path

from . import views

urlpatterns = [
    path('', views.mybattle, name='mybattle'),
    path('mybattle', views.mybattle, name='mybattle'),
    path('guildbattle', views.guildbattle, name='guildbattle')
]