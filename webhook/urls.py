from django.urls import path, include
from webhook import views
from rest_framework.routers import DefaultRouter
from webhook import views

router = DefaultRouter()
router.register(r'endpoints', views.EndpointViewSet, basename='endpoint')
router.register(r'request-logs', views.RequestLogViewSet, basename='request_log')
urlpatterns = [
    path('', include(router.urls)),
    path('webhook/<uuid:token>/', views.CaptureView.as_view())
]
