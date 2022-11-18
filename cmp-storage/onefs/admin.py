from django.contrib import admin
from .models import NFS


@admin.register(NFS)
class NFSAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'subnet_id', 'tenant_id', 'cidr', 'vlan_id',
                    'ip', 'network_id', 'status', 'region',
                    'nfs_id', 'quota_id')
