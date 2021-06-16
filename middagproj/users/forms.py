from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from .models import Profile
from .models import Allergy


# Inherit fra UserCreationForm

class UserRegisterForm(UserCreationForm):
    email = forms.EmailField()

    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']


class ProfileForm(forms.ModelForm):
    address = forms.CharField()
    allergies = forms.ModelMultipleChoiceField(widget=forms.CheckboxSelectMultiple,
                                               required=False,
                                               queryset=Allergy.objects.all())

    class Meta:
        model = Profile
        fields = ['address', 'allergies']
