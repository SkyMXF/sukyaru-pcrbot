from django.contrib import admin
from .models import TitleName, Title, UserTitle, Announcement

# Register your models here.
admin.site.register(TitleName)
admin.site.register(Title)
admin.site.register(UserTitle)
admin.site.register(Announcement)