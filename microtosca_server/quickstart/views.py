from django.shortcuts import render
from rest_framework import viewsets
from rest_framework.response import Response

from .serializers import ServiceSerializer

# Create your views here.

class ServiceViewSet(viewsets.ViewSet):
    # Required for the Browsable API renderer to have a nice form.
    serializer_class = ServiceSerializer

    def list(self, request):
        # serializer = ServiceSerializer(
        #     instance=services.values(), many=True)
        return Response(23)