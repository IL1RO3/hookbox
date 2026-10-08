from django.forms import fields, model_to_dict
from django.utils import timezone
from django.utils.autoreload import request_finished
from rest_framework import serializers
from rest_framework.relations import PrimaryKeyRelatedField
from webhook.models import Endpoint, RequestLog

class EndpointSerializer(serializers.ModelSerializer):
    owner = serializers.ReadOnlyField(source='owner.username')
    class Meta:
        model = Endpoint
        fields = ['expiration_date','owner','name', 'created_at','token', 'revoked','mock_status', 'mock_body', 'mock_enabled']

    def validate_expiration_date(self, value):
        if value is not None and value < timezone.now():
            raise serializers.ValidationError(
                "Invalid Expiration Date!"
            )
        return value



class RequestLogSerializer(serializers.ModelSerializer):
    class Meta:
        model = RequestLog
        fields = [
            'id',
            'request_duration',
            'method',
            'headers', 
            'query_params', 
            'payload', 
            'received_at', 
            'client_ip',
            'content_type',
            'replay_results'
        ]

    request_duration = serializers.SerializerMethodField()

    def get_request_duration(self, obj):
        if obj.request_duration is None:
            return None

        return round(obj.request_duration.total_seconds() * 1000, 2)


