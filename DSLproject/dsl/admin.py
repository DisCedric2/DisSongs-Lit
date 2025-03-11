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