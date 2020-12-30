from django.contrib import admin

from keyboard.models import DataCollectionSwipe


@admin.register(DataCollectionSwipe)
class DataCollectionSwipeAdmin(admin.ModelAdmin):
    list_display = ('user', 'target_text', 'is_trace_valid', 'created_on')

