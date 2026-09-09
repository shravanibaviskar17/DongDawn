from django.urls import path, include
from . import views


urlpatterns = [

    path(
        'next-difficulty/',
        views.get_next_difficulty,
        name='next_difficulty'
    ),

    path(
        'voice/',
        include('ai_engine.voice.urls')
    ),

]