from django.contrib import admin
from .models import Post , Tag , Comment , Like

# Register your models here.

@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    
    list_display = ('title' ,'user','create_at')
    search_fields = ('tags',)
    list_filter = ('user',)


@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    
    list_display = ('post' ,'user','parent','create_at')
    search_fields = ('post',)
    list_filter = ('parent',)


@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
    
    list_display = ('text' ,'slug','create_at')
    search_fields = ('text',)
    list_filter = ('slug',)


@admin.register(Like)
class LikeAdmin(admin.ModelAdmin):
    
    list_display = ('post' ,'user','create_at')
    list_filter = ('post',)