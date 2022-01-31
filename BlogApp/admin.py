from django.contrib import admin
from .models import *


@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = ('name', 'creation_date', 'user')
    list_filter = ('name', 'creation_date', 'user')


@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ('text', 'user', 'publication_date', 'post')
    list_filter = ('text', 'user', 'publication_date', 'post')
