from django.db import models
from django.conf import settings


class Caregiver(models.Model):

    user = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        null=True,
        blank=True
    )

    name = models.CharField(
        max_length=100
    )

    phone = models.CharField(
        max_length=15,
        blank=True
    )

    email = models.EmailField(
        blank=True
    )

    relationship = models.CharField(
        max_length=100,
        blank=True
    )

    patients = models.ManyToManyField(
        'patients.Patient',
        related_name='caregivers',
        blank=True
    )

    created_at = models.DateTimeField(
        auto_now_add=True
    )

    def __str__(self):
        return self.namepython 