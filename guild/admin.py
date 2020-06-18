from django.contrib import admin
from .models import Title, UserTitle, Announcement

# Register your models here.
admin.site.register(Title)
admin.site.register(UserTitle)
admin.site.register(Announcement)