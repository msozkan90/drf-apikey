from django.shortcuts import render

# Create your views here.
from rest_framework.views import APIView
from rest_framework.response import Response

from accounts.permissions import APIKeyPermission
import json
class ServiceAPIView(APIView):
    permission_classes = [APIKeyPermission]
    def get(self, request):
        # Custom GET functionality
        body = request.body.decode('utf-8')
        json_data = json.loads(body)
        try:
            func=json_data["a"]+json_data["b"]-json_data["c"]
            data = {
                'result': func,
            }
            return Response(data)
        except Exception as e:
            data = {
                'message': f'Error.{e}',
            }
            return Response(data)

    def post(self, request):
        # Custom POST functionality
        print(request.headers)
        data = {
            'message': 'This is a POST request.',
        }
        return Response(data)
