from django.urls import path

from . import views


urlpatterns = [

    path(
        "command/",
        views.process_voice_command,
        name="voice_command"
    ),

]