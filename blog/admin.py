from django.contrib import admin

from .models import Post, Comment

# Register your models here.


class PostAdmin(admin.ModelAdmin):
    list_display = ('title', 'slug', 'author', 'created', 'updated')
    list_filter = ('created', 'author')
    search_fields = ('title', 'body')
    prepopulated_fields = {'slug': ('title',)}


class CommentAdmin(admin.ModelAdmin):
    list_display = ('name', 'post', 'created',)
    list_filter = ('created',)
    search_fields = ('name', 'body')


admin.site.register(Post, PostAdmin)
admin.site.register(Comment, CommentAdmin)