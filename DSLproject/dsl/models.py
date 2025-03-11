from django.db import models
from django.contrib.auth.models import User

# Create your models here.

class AddSong(models.Model):
    title = models.CharField(max_length=200)
    artist = models.CharField(max_length=100)
    image = models.ImageField(upload_to='images/')
    video_url = models.URLField()
    
    def __str__(self):
        return f"{self.title} - {self.artist}"
    
class PremiumSubscription(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    payment_id = models.CharField(max_length=100, blank=True, null=True)
    subscription_status = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.user.username} - Premium: {self.subscription_status}"
    