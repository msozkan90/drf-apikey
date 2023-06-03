from rest_framework import  permissions
from rest_framework.exceptions import AuthenticationFailed
from rest_framework.permissions import BasePermission
from accounts.models import APIKey


class IsSelfOrAdmin(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        return request.user.is_superuser or obj == request.user
    
    
class APIKeyPermission(BasePermission):
    def has_permission(self, request, view):
        api_key = request.META.get('HTTP_X_API_KEY')

        try:
            api_key_object = APIKey.objects.get(key=api_key)
        except APIKey.DoesNotExist:
            raise AuthenticationFailed('Invalid API key.')

        # Save the API key object to the request for later use if needed
        request.api_key_object = api_key_object

        return True