from django.forms import ModelForm, ModelMultipleChoiceField, CheckboxSelectMultiple, TextInput
from django.utils import timezone
from users.models import Allergy
from .models import Event, Review
from .models import Comment


class EventForm(ModelForm):
    class Meta:
        model = Event
        fields = ['title', 'description', 'seats', 'place', 'date', 'time', 'ingredients', 'allergies', 'expense']  # '__all__'
        labels = {
            'title': 'Tittel',
            'description': 'Beskrivelse',
            'seats': 'Plasser',
            'place': 'Sted',
            'date': 'Dato',
            'time': 'Tid',
            'ingredients': 'Ingredienser',
            'allergies': 'Allergener',
            'expense': 'Utgifter',
        }
        widgets = {
            'date': TextInput(
                attrs={'type': 'date',
                       'min': timezone.now().date}
            ),
            'time': TextInput(
                attrs={'type': 'time',
                       'min': (timezone.now().strftime('%H:%M'))}
            ),
        }

    allergies = ModelMultipleChoiceField(queryset=Allergy.objects.all(), required=False, widget=CheckboxSelectMultiple)


class CommentForm(ModelForm):
    class Meta:
        model = Comment
        fields = ['content']


class ReviewForm(ModelForm):
    class Meta:
        model = Review
        fields = ['body', 'rating']
        labels = {
            'body': 'Tekst',
            'rating': 'Vurdering',
        }
