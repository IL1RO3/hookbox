
import django_filters

from webhook.models import RequestLog

class RequestLogFilter(django_filters.FilterSet):
    method = django_filters.CharFilter(
        field_name='method',
        lookup_expr='iexact',
    )

    ordering = django_filters.OrderingFilter(
        fields=(
            ('received_at', 'date'),
        ),
    )

    class Meta:
        model = RequestLog
        fields = ['method']
