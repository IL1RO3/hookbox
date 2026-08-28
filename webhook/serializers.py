from django.forms import fields, model_to_dict
from django.utils.autoreload import request_finished
from rest_framework import serializers
from rest_framework.relations import PrimaryKeyRelatedField
from webhook.models import Endpoint, RequestLog

class EndpointSerializer(serializers.ModelSerializer):
    owner = serializers.ReadOnlyField(source='owner.username')
    class Meta:
        model = Endpoint
        fields = ['owner','name', 'created_at','token']



class RequestLogSerializer(serializers.ModelSerializer):
    class Meta:
        model = RequestLog
        fields = ['method', 'headers', 'query_params', 'payload', 'received_at']
