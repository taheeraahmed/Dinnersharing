from dinnerevent.models import Event
from users.models import Allergy
from django.db.models import Q
from django.forms import CheckboxSelectMultiple
from django_filters import FilterSet, CharFilter, ModelMultipleChoiceFilter, NumberFilter


class EventFilter(FilterSet):
    search = CharFilter(method='event_search_filter', label='')
    allergies = ModelMultipleChoiceFilter(widget=CheckboxSelectMultiple, queryset=Allergy.objects.all(), exclude='True')
    seats = NumberFilter(method='event_seats_filter', label='')

    class Meta:
        model = Event
        fields = ['search', 'seats', 'allergies']

    # noinspection PyMethodMayBeStatic
    def event_search_filter(self, queryset, name, value):
        return Event.objects.filter(
            Q(title__icontains=value) | Q(description__icontains=value) | Q(ingredients__icontains=value)
        )

    # noinspection PyMethodMayBeStatic
    def event_seats_filter(self, queryset, name, value):
        return Event.objects.filter(
            Q(seats__lte=value)
        )
