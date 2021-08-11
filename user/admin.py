from django.contrib import admin
from .models import Guest


@admin.register(Guest)
class GuestAdmin(admin.ModelAdmin):
    list_display = ('name', 'date_created', 'email')
    list_filter = ('name', 'date_created', 'email')
