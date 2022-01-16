from django.contrib import admin
from .models import Guest
from datetime import datetime, timezone


@admin.action(description='Ban')
def ban_users(modeladmin, request, queryset):
    queryset.update(is_banned=True, last_ban_date=datetime.now(timezone.utc))


@admin.action(description='Mute')
def mute_users(modeladmin, request, queryset):
    queryset.update(is_muted=True)


@admin.action(description='Unban')
def unban_users(modeladmin, request, queryset):
    queryset.update(is_banned=False, last_ban_date=datetime.now(timezone.utc))


@admin.action(description='Unmute')
def unmute_users(modeladmin, request, queryset):
    queryset.update(is_muted=False)


@admin.register(Guest)
class GuestAdmin(admin.ModelAdmin):
    list_display = ('name', 'date_created', 'email', 'is_muted', 'is_banned', 'is_moderator', 'user')
    list_filter = ('date_created', 'email', 'is_moderator', 'last_ban_date')
    actions = [ban_users, mute_users, unmute_users, unban_users]
