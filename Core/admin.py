from django.contrib import admin
from .models import Image

# Register your models here.

@admin.register(Image)
class ImageAdmin(admin.ModelAdmin):

    list_display = ('name' , 'Image', 'is_default', 'create_at')
    list_filter = ('is_default',)
    search_fields = ('name',)