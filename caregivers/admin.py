from django.contrib import admin
from .models import Caregiver


@admin.register(Caregiver)
class CaregiverAdmin(admin.ModelAdmin):

    list_display = (
        'name',
        'phone',
        'email',
        'relationship',
        'created_at',
    )

    search_fields = (
        'name',
        'phone',
        'email',
    )

    ordering = (
        'name',
    )