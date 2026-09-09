from django.db import models


class Reminder(models.Model):

    REMINDER_TYPES = [
        ('medicine', 'Medicine'),
        ('water', 'Water'),
        ('meal', 'Meal'),
        ('appointment', 'Doctor Appointment'),
        ('activity', 'Daily Activity'),
    ]

    patient = models.ForeignKey(
        'patients.Patient',
        on_delete=models.CASCADE,
        related_name='reminders'
    )

    title = models.CharField(
        max_length=200
    )

    reminder_type = models.CharField(
        max_length=20,
        choices=REMINDER_TYPES
    )

    description = models.TextField(
        blank=True
    )

    reminder_time = models.TimeField()

    reminder_date = models.DateField(
        null=True,
        blank=True
    )

    is_completed = models.BooleanField(
        default=False
    )

    created_at = models.DateTimeField(
        auto_now_add=True
    )

    def __str__(self):

        return f"{self.patient.name} - {self.title}"