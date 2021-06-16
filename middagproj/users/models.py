from django.db import models
from django.contrib.auth.models import User


class Allergy(models.Model):
    allergy = models.CharField(max_length=50)

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['allergy'], name='unique_allergy')
        ]

    def __str__(self):
        return self.allergy


class Profile(models.Model):
    # CASCADE deletes the profile when the user is deleted
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    address = models.CharField(max_length=50, blank=True)
    allergies = models.ManyToManyField(Allergy, blank="True")
    events = models.ManyToManyField('dinnerevent.Event', blank="True")

    class Meta:
        verbose_name = 'Profil'
        verbose_name_plural = 'Profiler'

    def __str__(self):
        return f'{self.user.username} Profile'
