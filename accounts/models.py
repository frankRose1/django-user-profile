from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver

# Create your models here.


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    first_name = models.CharField(max_length=255, blank=True)
    last_name = models.CharField(max_length=255, blank=True)
    email = models.EmailField(max_length=255, blank=True)
    is_new = models.BooleanField(default=True)
    bio = models.TextField(max_length=1500, help_text='Tell us a bit about yourself.', blank=True)
    date_of_birth = models.DateField(
            null=True,
            blank=True,
            help_text='Please use one of the following formats: YYYY-MM-DD, MM/DD/YYYY, MM/DD/YY'
    )
    avatar = models.ImageField(
        blank=True,
        null=True,
        upload_to='avatars'
    )


@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)


@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    instance.profile.save()
