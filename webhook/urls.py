from django.urls import path, include
from webhook import views
from rest_framework.routers import DefaultRouter
from webhook import views

router = DefaultRouter()
router.register(r'endpoint', views.EndpointViewSet, basename='endpoint')

urlpatterns = [
    path('', include(router.urls)),
    
]
