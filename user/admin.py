from django.contrib import admin
from .models import UserInfo, UserGroup

# Register your models here.
admin.site.register(UserInfo)
admin.site.register(UserGroup)