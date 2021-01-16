from django.contrib import admin

from competition.models import Submission


@admin.register(Submission)
class SubmissionAdmin(admin.ModelAdmin):
    list_display = ('user', 'description', 'top1_accuracy', 'top3_accuracy')
