from rest_framework import serializers
from webhook.models import Endpoint

class EndpointSerializer(serializers.ModelSerializer):
    class Meta:
        model = Endpoint
        fields = ['owner','name', 'created_at','token']


