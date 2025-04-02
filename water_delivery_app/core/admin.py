from django.contrib import admin
from .models import Schedule

@admin.register(Schedule)
class ScheduleAdmin(admin.ModelAdmin):
    list_display = ['user', 'frequency', 'next_delivery_date', 'jugs_per_delivery','delivery_status', 'subscription']
    list_filter = ['delivery_status', 'frequency', 'event_date']
    search_fields = ['event_name', 'user__username']
