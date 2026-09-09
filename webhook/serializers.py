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
        fields = ['expiration_date','owner','name', 'created_at','token', 'revoked']

    def validate_expiration_date (self, value):
        if value < timezone.localtime():
            raise serializers.ValidationError(
                "Invalid Expiration Date!"
            )
        return value



class RequestLogSerializer(serializers.ModelSerializer):
    class Meta:
        model = RequestLog
        fields = ['method', 'headers', 'query_params', 'payload', 'received_at', 'client_ip','content_type']
