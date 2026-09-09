from django.db import models

class GameResult(models.Model):

    patient = models.ForeignKey(
        'patients.Patient',
        on_delete=models.CASCADE,
        related_name='game_results',
        blank=True,
        null=True
    )

    DIFFICULTY_CHOICES = [
        ('easy', 'Easy'),
        ('medium', 'Medium'),
        ('hard', 'Hard'),
    ]

    game_name = models.CharField(max_length=100)

    score = models.IntegerField(default=0)

    attempts = models.IntegerField(default=0)

    accuracy = models.FloatField(default=0.0)

    difficulty = models.CharField(
        max_length=20,
        choices=DIFFICULTY_CHOICES,
        default='easy'
    )

    completion_time = models.FloatField(default=0.0)

    played_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.game_name} - {self.score}"