from django.contrib import admin

from .models import Event, Comment, Review

admin.site.register(Event)
admin.site.register(Comment)
admin.site.register(Review)
