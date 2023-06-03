from django.db import models
from django.contrib.auth.models import User
# User Modelinin Email Alanını Zorunlu ve Unique Yapma
User._meta.get_field('email').blank = False
User._meta.get_field('email')._unique = True


# Create your models here.
class APIKey(models.Model):
    key = models.CharField(max_length=255, unique=True)
    company = models.OneToOneField(User, on_delete=models.CASCADE, related_name='apikey')  
    request_limit = models.IntegerField(null=True, blank=True)
    expiration_date = models.DateTimeField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    def __str__(self):
        return self.key
