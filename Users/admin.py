from django.contrib import admin
from .models import User , Follow 

# Register your models here.

@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    
    list_display = ('username' ,'phone_number','create_at')
    search_fields = ('username',)


@admin.register(Follow)
class FollowAdmin(admin.ModelAdmin):
    
    list_display = ('following_user' , 'follower_user', 'create_at')
    list_filter = ('following_user',)

