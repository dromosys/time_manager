from django.contrib import admin

# Register your models here.
from .models import time_entry

class TimeEntryAdmin(admin.ModelAdmin):
    readonly_fields = ('created_at','updated_at')

admin.site.register(time_entry, TimeEntryAdmin)