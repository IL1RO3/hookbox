
from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.views import APIView
from webhook.models import Endpoint, RequestLog
from rest_framework.response import Response
from webhook.serializers import EndpointSerializer, RequestLogSerializer
from django.utils.decorators import method_decorator
from rest_framework.decorators import action
from django.views.decorators.csrf import csrf_exempt
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import SearchFilter, OrderingFilter
# Create your views here.

class EndpointViewSet(viewsets.ModelViewSet):
    queryset = Endpoint.objects.all().order_by('-created_at')
    serializer_class = EndpointSerializer
    permission_classes = [IsAuthenticated]
    filter_backends = [
        SearchFilter,
        OrderingFilter
    ]

    search_fields = [
        "name"
    ] 

    ordering_fields = [
        "created_at"
    ]

    @action(detail=True, methods=['get'])
    def requests(self, request, pk=None):
        endpoint = self.get_object()

        queryset = RequestLog.objects.filter(endpoint=endpoint)
        
        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = RequestLogSerializer(
                 page,
                 many=True
            )
            return self.get_paginated_response(serializer.data)

        serializer = RequestLogSerializer(
             queryset,
             many=True
        )

        return Response(serializer.data)


@method_decorator(csrf_exempt, name='dispatch')
class CaptureView(APIView):
    authentication_classes = []
    permission_classes = [AllowAny]
  
    def handle_request(self, request, token):
        endpoint = Endpoint.objects.get(token=token)

        request_log = RequestLog.objects.create(
            endpoint=endpoint,
            method=request.method,
            headers=dict(request.headers),
            query_params=request.query_params,
            payload=request.body.decode()
        )

        return Response({'recived': True})

    
    def get(self, request, token):
        return self.handle_request(request, token)

    def post(self, request, token):
        return self.handle_request(request, token)
 
    def put(self, request, token):
        return self.handle_request(request, token)

    def patch(self, request, token):
        return self.handle_request(request, token)

    def delete(self, request, token):
        return self.handle_request(request, token)

class RequestLogViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = RequestLog.objects.all()
    serializer_class = RequestLogSerializer
    permission_classes = [IsAuthenticated]
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ["method", "endpoint"]
