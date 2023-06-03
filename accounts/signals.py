from django.dispatch import receiver
from accounts.models import  APIKey
from django.contrib.auth.models import User
from django.db.models.signals import post_save
import secrets
from django.utils import timezone
from datetime import timedelta
# User Profile Signals
@receiver(post_save, sender=User)
def create_user_apikey(sender, instance, created, **kwargs):
    if created:
        # Generate a unique API key
        api_key = secrets.token_hex(32)
        
        # Set expiration date to one year from now
        expiration_date = timezone.now() + timedelta(days=365)
        
        # Set the request limit for the API key
        request_limit = 1000  # You can adjust this as needed
        
        APIKey.objects.create(company=instance, key=api_key, expiration_date=expiration_date, request_limit=request_limit)

@receiver(post_save, sender=User)
def save_user_apikey(sender, instance, **kwargs):
    instance.apikey.save()