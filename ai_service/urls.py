from django.urls import path
from ai_service.views import ServiceAPIView

urlpatterns = [
    path('ai/service/', ServiceAPIView.as_view(), name='ai_service'),
]
