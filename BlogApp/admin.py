from django.contrib import admin
from .models import *


@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = ('name', 'creation_date', 'user')
    list_filter = ('name', 'creation_date', 'user')


@admin.register(Guest)
class GuestAdmin(admin.ModelAdmin):
    list_display = ('name', 'date_created', 'email')
    list_filter = ('name', 'date_created', 'email')


@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ('author', 'publication_date', 'post')
    list_filter = ('author', 'publication_date', 'post')
