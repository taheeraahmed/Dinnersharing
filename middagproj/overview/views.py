from django.shortcuts import render
from dinnerevent.models import Event
from django.contrib.auth.models import User
from .filters import EventFilter


# renders what we want user to se when entering this route
def home(request):
    events = Event.objects.all()
    events_filter = EventFilter(request.GET, queryset=events)
    return render(request, 'overview/overview.html', {'events_filter': events_filter})
    # renders overview.html template


def contact(request):
    names = User.objects.filter(is_superuser=True)
    return render(request, 'overview/contact.html', {'displaysuperusers': names})
