from django.urls import path
from . import views
from .views import EventDetail, EventDelete, EventCreate, EventUpdate, ReviewCreate


app_name = 'event'

urlpatterns = [
    path('join/<int:pk>', views.join_event, name="join"),
    path('unjoin/<int:pk>', views.unjoin_event, name="unjoin"),
    path('', EventCreate.as_view(), name='eventform'),
    path('<int:pk>/', EventDetail.as_view(), name='eventdetail'),
    path('<int:pk>/review', ReviewCreate.as_view(), name='review-create'),
    path('<int:pk>/delete/', EventDelete.as_view(), name='event-delete'),
    path('<int:pk>/update', EventUpdate.as_view(), name='event-update')
]
