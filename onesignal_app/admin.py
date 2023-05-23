from django.contrib import admin
from .models import *


@admin.register(OneSignalDevice)
class OneSignalDeviceAdmin(admin.ModelAdmin):
    list_display = ['user', 'device_id', 'device_type', 'app_id', 'created', 'updated']
    autocomplete_fields = ['user']
