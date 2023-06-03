from rest_framework import  permissions
from rest_framework.exceptions import AuthenticationFailed
from rest_framework.permissions import BasePermission
from accounts.models import APIKey
from django.utils import timezone

class IsSelfOrAdmin(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        key= APIKey.objects.filter(key=request.headers['X-Api-Key']).first()
        return key.company.is_superuser or obj == key.company
    
    
class APIKeyPermission(BasePermission):
    def has_permission(self, request, view):
        api_key = request.META.get('HTTP_X_API_KEY')

        try:
            api_key_object = APIKey.objects.get(key=api_key)
        except APIKey.DoesNotExist:
            raise AuthenticationFailed('Invalid API key.')

        if api_key_object.expiration_date is not None and api_key_object.expiration_date < timezone.now():
            raise AuthenticationFailed('API key has expired.')

        if api_key_object.request_limit is not None and api_key_object.request_limit <= 0:
            raise AuthenticationFailed('API key has reached the request limit.')

        if api_key_object.request_limit is not None:
            api_key_object.request_limit -= 1
            api_key_object.save()
        # Save the API key object to the request for later use if needed
        request.api_key_object = api_key_object

        return True