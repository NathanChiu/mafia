from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver

class PlayerProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    alias = models.CharField(max_length=100)
    nums = models.IntegerField(default=0)

# connect this function to occur whenever post_save signal is triggered
@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    #when a new record is created
    if created:
        PlayerProfile.objects.create(user=instance)

# tie the profile save to the user save.
@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    instance.playerprofile.save()
