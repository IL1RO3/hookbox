from django.contrib import admin
from .models import RequestLog, Endpoint

# Register your models here.
class RequestLogInline(admin.TabularInline):
    model = RequestLog
    extra = 1
    readonly_fields = [
        "method",
        "headers",
        "query_params",
        "payload",
        "received_at",
        "client_ip",
        'content_type',
        'replay_results',
    ]
    can_delete = False

    
class EndpointAdmin(admin.ModelAdmin):
    fields = ['name', 'revoked','expiration_date']
    list_display = ['name' , 'revoked' , 'expiration_date']
    inlines= [RequestLogInline]
    

class RequestLogAdmin(admin.ModelAdmin):
    list_display = ['id','endpoint_name', 'received_at' , 'method']
    readonly_fields = [
        field.name for field in RequestLog._meta.fields
    ]

    def has_add_permission(self, request, obj=None):
        return False

    def has_change_permission(self, request, obj=None):
        return False

    def endpoint_name(self, obj):
        return obj.endpoint.name


admin.site.register(Endpoint ,EndpointAdmin)
admin.site.register(RequestLog, RequestLogAdmin)
