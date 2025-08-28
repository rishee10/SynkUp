from django.contrib import admin

# Register your models here.

from django.contrib import admin
from .models import Job

@admin.register(Job)
class JobAdmin(admin.ModelAdmin):
    list_display = ('title', 'company', 'location', 'job_type', 'work_mode', 'posted_at', 'is_active')
    list_filter = ('job_type', 'work_mode', 'is_active', 'posted_at')
    search_fields = ('title', 'company', 'location', 'skills')
    fieldsets = (
        ('Basic Info', {'fields': ('title', 'company', 'official_link', 'description')}),
        ('Job Details', {'fields': ('job_type', 'work_mode', 'location', 'salary')}),
        ('Requirements', {'fields': ('requirements', 'skills')}),
        ('Application', {'fields': ('application_link', 'is_active')}),
    )
