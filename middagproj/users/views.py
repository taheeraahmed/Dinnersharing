from django.db.models import Avg
from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from dinnerevent.models import Review
from .forms import UserRegisterForm, ProfileForm


def register(request):
    if request.method == "POST":
        form = UserRegisterForm(request.POST)
        profile_form = ProfileForm(request.POST)
        if form.is_valid() and profile_form.is_valid():
            user = form.save()
            user_profile = profile_form.save(commit=False)
            user_profile.user = user
            user_profile.save()
            profile_form.save_m2m()
            username = form.cleaned_data.get('username')
            messages.success(request, f'Bruker er laget for {username}')
            return redirect('login')
    else:
        form = UserRegisterForm()
        profile_form = ProfileForm()
    return render(request, 'users/register.html', {'form': form, 'profile_form': profile_form})


@login_required
def profile(request, pk):  # Denne viser profilen til brukerene
    all_user_reviews = Review.objects.filter(event__user=User.objects.get(pk=pk))
    avg_rating = all_user_reviews.aggregate(Avg('rating')).get('rating__avg')
    return render(request, 'users/profile.html', {
        'reviews': all_user_reviews,
        'score': rounded_rating(avg_rating),
        'user_profile': User.objects.get(pk=pk),
    })


def rounded_rating(number):
    """Round a number to closet 1/2 integer"""
    if number is not None:
        return round(number * 2) / 2
    return None
