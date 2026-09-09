from django.contrib import admin
from .models import Reminder


@admin.register(Reminder)
class ReminderAdmin(admin.ModelAdmin):

    list_display = (
        'patient',
        'title',
        'reminder_type',
        'reminder_time',
        'reminder_date',
        'is_completed',
        'created_at',
    )

    list_filter = (
        'reminder_type',
        'is_completed',
        'reminder_date',
    )

    search_fields = (
        'patient__name',
        'title',
    )

    ordering = (
        'reminder_date',
        'reminder_time',
    )