# Library
from rest_framework import status,viewsets, permissions,response,exceptions
from django.shortcuts import get_object_or_404
# Model
from accounts.models import User,APIKey
# Serializers
from accounts.serializers import UserSerializer,UserAPIkeySerializer
# Utils
from accounts.permissions import APIKeyPermission,IsSelfOrAdmin

class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    def get_permissions(self):
        if self.action == 'retrieve':
            self.permission_classes = [APIKeyPermission]
        elif self.action in ['update', 'partial_update', 'destroy']:
            self.permission_classes = [IsSelfOrAdmin,APIKeyPermission]
        else:
            self.permission_classes = [permissions.AllowAny]
        return super().get_permissions()

    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance)
        api_serializer = UserAPIkeySerializer(instance.apikey)
        serializer.data['apikey'] = api_serializer.data

        return response.Response(serializer.data)

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        self.perform_destroy(instance)
        return response.Response(status=status.HTTP_204_NO_CONTENT)

class APIKeyViewSet(viewsets.ModelViewSet):
    queryset = APIKey.objects.all()
    serializer_class = UserAPIkeySerializer


