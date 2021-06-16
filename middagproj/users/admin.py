from django.contrib import admin
from .models import Profile
from django.contrib.auth.models import Group

# Register your models here.

#Adds profile section to admin-site
admin.site.register(Profile)

#removes Group from admin-site
admin.site.unregister(Group)

