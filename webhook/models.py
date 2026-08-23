
from django.db import models
from django.contrib.auth.models import User
from django.dispatch import receiver
import uuid

# Create your models here.

class Endpoint(models.Model):
    owner = models.ForeignKey(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=200)
    token = models.UUIDField(unique=True, editable=False, default=uuid.uuid4)
    created_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f'name: {self.name}\ntoken: {self.token}'


class RequestLog(models.Model):
    endpoint = models.ForeignKey(Endpoint, on_delete=models.CASCADE)
    method = models.JSONField()
    headers = models.JSONField()
    query_params = models.JSONField()
    payload = models.TextField()
    received_at = models.DateTimeField(auto_now_add=True)
