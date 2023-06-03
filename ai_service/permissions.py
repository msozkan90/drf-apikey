from rest_framework import  permissions
from rest_framework.authentication import BaseAuthentication
from rest_framework.exceptions import AuthenticationFailed
from rest_framework.permissions import BasePermission
from accounts.models import APIKey
# ViewSets define the view behavior.
class IsSelfOrAdmin(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        return request.user.is_superuser or obj == request.user
    

from rest_framework_simplejwt.authentication import JWTAuthentication

class APIKeyPermission(BasePermission):
    def has_permission(self, request, view):
        api_key = request.META.get('HTTP_X_API_KEY')
        access_token = request.META.get('HTTP_AUTHORIZATION')
        jwt_authentication = JWTAuthentication()
        user, _ = jwt_authentication.authenticate(request)
        if not api_key or not access_token:
            return False

        try:
            api_key_object = APIKey.objects.get(key=api_key, user=user)
        except APIKey.DoesNotExist:
            return False

        # Save the API key object to the request for later use if needed
        request.api_key_object = api_key_object

        return True

class APIKeyAuthentication(BaseAuthentication):
    def authenticate(self, request):
        if not APIKeyPermission().has_permission(request, self):
            raise AuthenticationFailed('Invalid API key or access token.')

        api_key_object = request.api_key_object

        # Return a tuple of (user, api_key_object) if the authentication is successful
        return (api_key_object.user, api_key_object)