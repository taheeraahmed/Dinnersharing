from django.urls import path
from . import views  # . means current dir

urlpatterns = [
    path('', views.home, name='overview-home'),
    path('contact', views.contact, name='contact'),
]
