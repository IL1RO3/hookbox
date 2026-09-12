import uuid
import httpx
from django.forms.utils import timezone
from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.views import APIView, status
from webhook.filters import RequestLogFilter
from webhook.models import Endpoint, RequestLog
from rest_framework.response import Response
from webhook.serializers import EndpointSerializer, RequestLogSerializer
from django.utils.decorators import method_decorator
from rest_framework.decorators import action
from django.views.decorators.csrf import csrf_exempt
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import SearchFilter, OrderingFilter

# endpoint viewset

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

    # nested /requests action

    @action(detail=True,methods=['get'])
    def requests(self, request, pk=None):
        endpoint = self.get_object()

        queryset = RequestLog.objects.filter(endpoint=endpoint)

        queryset = RequestLogFilter(
            request.query_params,
            queryset=queryset,
        ).qs
        
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


    # nested url path for rotation or revokation

    @action(detail=True, methods=['patch', 'delete'])
    def token(self, request, pk=None):
        endpoint = self.get_object()

        if request.method == 'PATCH':
            endpoint.token = uuid.uuid4()
            endpoint.save(update_fields=['token'])

            return Response({
                'message': 'Token rotation done!',
                'token' : endpoint.token,
            })

        elif request.method == 'DELETE':
            endpoint.revoked = True 
            endpoint.save(update_fields=['revoked'])

            return Response(
                 {"message": "Token revoked"},
                 status=status.HTTP_204_NO_CONTENT
            )

    
    def perform_create(self, serializer):
        return serializer.save(owner=self.request.user)

    def get_queryset(self):
        return Endpoint.objects.filter(owner=self.request.user)

    
          
# capture view to record requests

@method_decorator(csrf_exempt, name='dispatch')
class CaptureView(APIView):
    authentication_classes = []
    permission_classes = []
    
    # request handlers which is used for all methods explicitly

    def handle_request(self, request, token):
        try:
            endpoint = Endpoint.objects.get(token=token)
        except Endpoint.DoesNotExist:
            return Response({'message': 'Token was not found.'}, status=status.HTTP_404_NOT_FOUND)
        
        if endpoint.expiration_date:
            if endpoint.expiration_date >= timezone.localtime(timezone.now()):
                pass
            else:
                return Response({'message': 'Token is expired.'},status=status.HTTP_410_GONE)

        if endpoint.revoked:
            return Response({'message': 'Token is revoked.'}, status=status.HTTP_410_GONE)
        
        client_ip = request.META.get('REMOTE_ADDR')

        request_log = RequestLog.objects.create(
            endpoint=endpoint,
            method=request.method,
            headers=dict(request.headers),
            query_params=request.query_params,
            payload=request.body.decode(),
            client_ip=client_ip,
            content_type = request.content_type
        )

        return Response({'recived': True}, status=status.HTTP_201_CREATED)
    

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


# requestlog views which holds all records

class RequestLogViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = RequestLog.objects.all()
    serializer_class = RequestLogSerializer
    permission_classes = [IsAuthenticated]
    filter_backends = [DjangoFilterBackend, OrderingFilter]
    filterset_fields = ["method", "endpoint"]
    ordering_fields = ['received_at']

    def get_queryset(self):
        return RequestLog.objects.filter(endpoint__owner=self.request.user)


    @action(detail=True, methods=['post'])
    def replay(self,request,pk=None):
        destination_url = request.data.get('url')
        request_obj = self.get_object()

        excluded = {
            "host",
            "content-length",
            "connection",
            "keep-alive",
            "proxy-connection",
            "transfer-encoding",
            "te",
            "trailer",
            "upgrade",
        }
    
        headers = {
            key: value
            for key, value in request_obj.headers.items()
            if key.lower() not in excluded
        }

        response = httpx.request(
            method=request_obj.method,
            url=destination_url,
            headers=headers,
            params=request_obj.query_params,
            content=request_obj.payload,
        )

        result = {
            "destination_url": destination_url,
            "status_code": response.status_code,
            "headers": dict(response.headers),
            "body": response.text,
            "replayed_at": timezone.localtime().isoformat(),
        }

        request_obj.replay_results.append(result)
        request_obj.save(update_fields=['replay_results'])

        return Response({
            "status_code": response.status_code,
            "headers": dict(response.headers),
            "body": response.text,
        })

          
