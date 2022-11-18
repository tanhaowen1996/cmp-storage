from rest_framework import serializers
from .models import NFS


class NFSSerializer(serializers.ModelSerializer):
    id = serializers.CharField(required=False)
    name = serializers.CharField(required=False)
    subnet_id = serializers.CharField(required=False)
    tenant_id = serializers.CharField(required=False)
    cidr = serializers.CharField(required=False)
    vlan_id = serializers.IntegerField(required=False)
    ip = serializers.CharField(required=False)
    network_id = serializers.CharField(required=False)
    status = serializers.CharField(required=False)
    nfs_id = serializers.IntegerField(required=False)
    quota_id = serializers.CharField(required=False)

    class Meta:
        model = NFS
        fields = '__all__'


