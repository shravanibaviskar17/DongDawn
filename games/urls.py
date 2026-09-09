from django.urls import path
from . import views


urlpatterns = [

    path(
        '',
        views.memory_game,
        name='memory_game'
    ),

    path(
        'save-result/',
        views.save_game_result,
        name='save_game_result'
    ),

    path(
        'routine/',
        views.routine_game,
        name='routine_game'
    ),

    path(
        'object/',
        views.object_game,
        name='object_game'
    ),

    path(
        'pattern/',
        views.pattern_game,
        name='pattern_game'
    ),

    path(
        'attention/',
        views.attention_game,
        name='attention_game'
    ),

    path(
        'emotion/',
        views.emotion_game,
        name='emotion_game'
    ),

]