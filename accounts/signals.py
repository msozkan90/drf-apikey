from django.dispatch import receiver
from accounts.models import  APIKey
from django.contrib.auth.models import User
from django.db.models.signals import post_save
import secrets
# User Profile Signals
@receiver(post_save, sender=User)
def create_user_apikey(sender, instance, created, **kwargs):
    if created:
        # Generate a unique API key
        api_key = secrets.token_hex(32)
        APIKey.objects.create(company=instance,key=api_key)

@receiver(post_save, sender=User)
def save_user_apikey(sender, instance, **kwargs):
    instance.apikey.save()
