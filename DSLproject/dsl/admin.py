from django.contrib import admin
from .models import AddSong

# Register your models here.
class AddSongAdmin(admin.ModelAdmin):
    list_display = [
        "title",
        "artist",
        "image",
        "video_url",
    ]

class UpSongAdmin(admin.ModelAdmin):
    list_display = [
        'title', 'artist', 'uploaded_by',
    ]
    search_fields = [
        'title', 'artist', 'uploaded_by__username',
    ]

admin.site.register(AddSong, AddSongAdmin)