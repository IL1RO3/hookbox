
from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from webhook.models import Endpoint
from webhook.serializers import EndpointSerializer 
# Create your views here.

class EndpointViewSet(viewsets.ModelViewSet):
    queryset = Endpoint.objects.all().order_by('-created_at')
    serializer_class = EndpointSerializer
    permission_classes = [IsAuthenticated]

    
