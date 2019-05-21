import django_filters
from api.models import Email


class EmailDateFilter(django_filters.FilterSet):
    date_from = django_filters.DateTimeFilter(field_name='date', lookup_expr='gte')
    date_to = django_filters.DateTimeFilter(field_name='date', lookup_expr='lte')

    sent_date_from = django_filters.DateTimeFilter(field_name='sent_date', lookup_expr='gte')
    sent_date_to = django_filters.DateTimeFilter(field_name='sent_date', lookup_expr='lte')

    class Meta:
        model = Email
        fields = ('sent_date', 'date')
