
from django.db import models
from django.contrib.auth.models import User
from django.db.models.base import model_unpickle
from django.dispatch import receiver
import uuid
from django.db.models import Q
from httpx._transports import default


# Create your models here.

class Endpoint(models.Model):
    owner = models.ForeignKey(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=200)
    token = models.UUIDField(unique=True, editable=False, default=uuid.uuid4)
    created_at = models.DateTimeField(auto_now=True)
    expiration_date = models.DateTimeField(default=None, blank=True, null=True)
    revoked = models.BooleanField(default=False)
    mock_enabled = models.BooleanField(default=False)
    mock_status = models.IntegerField(blank=True, null=True)
    mock_body = models.JSONField(blank=True,null=True)
    
    def __str__(self):
        return f'name: {self.name}\ntoken: {self.token}'

    class Meta:
        constraints = [
            models.CheckConstraint(
                condition=Q(mock_status__gte=100) & Q(mock_status__lte=599),
                name="valid_http_status_code", 
            )
        ]
    
   

class RequestLog(models.Model):
    endpoint = models.ForeignKey(Endpoint, on_delete=models.CASCADE)
    method = models.CharField(max_length=10)
    headers = models.JSONField()
    query_params = models.JSONField()
    payload = models.TextField()
    received_at = models.DateTimeField(auto_now_add=True)
    client_ip = models.GenericIPAddressField(default='0.0.0.0')
    content_type = models.CharField(null=True, blank=True)
    replay_results = models.JSONField(default=list,blank=True)
    request_duration = models.DurationField(blank=True,null=True)

    
