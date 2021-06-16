from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
from django.urls import reverse
from django.core.validators import MaxValueValidator
from users.models import Allergy


class Event(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=150)
    description = models.TextField(max_length=500)
    seats = models.PositiveIntegerField(default=1)
    place = models.CharField(max_length=50)
    expense = models.PositiveIntegerField(default=0)
    date = models.DateField(default=timezone.now)
    time = models.TimeField(default=timezone.now)
    ingredients = models.TextField(max_length=500)
    allergies = models.ManyToManyField(Allergy)
    guests = models.ManyToManyField(User, related_name="event_guests")

    class Meta:
        verbose_name = 'Arrangement'
        verbose_name_plural = 'Arrangement'

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('eventdetail', kwargs={'pk': self.pk})


class Comment(models.Model):
    event = models.ForeignKey(Event, on_delete=models.CASCADE, related_name='comments')
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    content = models.TextField(max_length=500)
    created_on = models.DateTimeField(default=timezone.now)

    class Meta:
        verbose_name = 'Kommentar'
        verbose_name_plural = 'Kommentarer'

    def __str__(self):
        return self.content


class Review(models.Model):
    RATINGS = (
        (0, "0"),
        (1, "1"),
        (2, "2"),
        (3, "3"),
        (4, "4"),
        (5, "5"),
    )

    event = models.ForeignKey(Event, on_delete=models.CASCADE, related_name="reviews")
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    body = models.TextField(max_length=500)
    rating = models.PositiveIntegerField(
        validators=[
            MaxValueValidator(5)
        ],
        choices=RATINGS,
    )
    created_on = models.DateTimeField(default=timezone.now)

    class Meta:
        verbose_name = 'Anmeldelse'
        verbose_name_plural = 'Anmeldelser'

    def __str__(self):
        return 'by {user}: gave Rating: {rating} to event {event}'.format(user=self.user, rating=self.rating,
                                                                          event=self.event)
