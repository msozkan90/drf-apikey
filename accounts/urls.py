from django.urls import path, include
from rest_framework.routers import DefaultRouter
from accounts.views import APIKeyViewSet,UserViewSet


router = DefaultRouter()
router.register(r'apikey', APIKeyViewSet)
router.register(r'account', UserViewSet)

urlpatterns = [
    path('', include(router.urls)),
]