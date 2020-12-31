from django.contrib import admin

from keyboard.models import DataCollectionSwipe


@admin.register(DataCollectionSwipe)
class DataCollectionSwipeAdmin(admin.ModelAdmin):
    list_display = ('user', 'id', 'target_text', 'trace_matches_text', 'created_on')
