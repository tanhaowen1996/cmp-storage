from django_filters import (
    FilterSet,
    CharFilter)
from .models import NFS


class NFSFilter(FilterSet):
    id = CharFilter(field_name='id', lookup_expr='icontains')
    name = CharFilter(field_name='name', lookup_expr='icontains')
    tenant_id = CharFilter(field_name='tenant_id', lookup_expr='icontains')
    tenant_name = CharFilter(field_name='tenant_name', lookup_expr='icontains')
    ip = CharFilter(field_name='ip', lookup_expr='icontains')
    region = CharFilter(field_name='region', lookup_expr='icontains')

    class Meta:
        mode = NFS
        filter = ('name', 'id', 'tenant_id', 'tenant_name', 'region', 'ip')
