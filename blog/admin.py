from django.contrib import admin
from .models import Post, Comment

class PostAdmin(admin.ModelAdmin):
	list_display = ['pk', 'title', 'author']
	list_display_links = ['pk', 'title']
	ordering = ['pk']
admin.site.register(Post, PostAdmin)

class CommentAdmin(admin.ModelAdmin):
	list_display = ['pk', 'author']
	list_display_links = ['pk']
	ordering = ['pk']
admin.site.register(Comment, CommentAdmin)
