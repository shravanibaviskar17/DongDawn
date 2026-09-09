from django.contrib import admin
from .models import GameResult


@admin.register(GameResult)
class GameResultAdmin(admin.ModelAdmin):

    list_display = (
        'game_name',
        'score',
        'attempts',
        'accuracy',
        'difficulty',
        'completion_time',
        'played_at',
    )

    list_filter = (
        'game_name',
        'difficulty',
        'played_at',
    )

    ordering = ('-played_at',)