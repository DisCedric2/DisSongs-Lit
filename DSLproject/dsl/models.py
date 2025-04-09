from django.db import models
from django.contrib.auth.models import User
from django.contrib.auth import get_user_model


# Create your models here.

User = get_user_model()

from django.utils import timezone
class AddSong(models.Model):
    title = models.CharField(max_length=200)
    artist = models.CharField(max_length=100)
    description = models.TextField(blank=True)
    genre = models.CharField(max_length=100, default="Unknown")
    lyrics = models.TextField(default='N/A', blank=True, null=True)
    image = models.ImageField(upload_to='images/')
    uploaded_by = models.ForeignKey(User, on_delete=models.CASCADE, default=1)
    video_url = models.URLField()
    upload_date = models.DateTimeField(default=timezone.now)
    click_count = models.IntegerField(default=0) #top chart counter
    
    
    def __str__(self):
        return f"{self.title} - {self.artist}"

class UpSong(models.Model):
    title = models.CharField(max_length=100)
    artist = models.CharField(max_length=100)
    description = models.TextField(blank=True)
    lyrics = models.TextField(default='N/A', blank=True, null=True)
    video_url = models.URLField(blank=True)
    image = models.ImageField(upload_to='songs/', blank=True)
    uploaded_by = models.ForeignKey(User, on_delete=models.CASCADE, default=1)
    upload_date = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return self.title


class PremiumSubscription(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    payment_id = models.CharField(max_length=100, blank=True, null=True)
    subscription_status = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.user.username} - Premium: {self.subscription_status}"

    @staticmethod
    def is_premium(user):
        """Returns True if the user is a premium member."""
        if user.is_authenticated:
            return PremiumSubscription.objects.filter(user=user, subscription_status=True).exists()
        return False