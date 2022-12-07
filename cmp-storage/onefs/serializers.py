from rest_framework import serializers
from .models import NFS


class NFSSerializer(serializers.ModelSerializer):
    id = serializers.CharField(required=False)
    name = serializers.CharField(required=False)
    subnet_id = serializers.CharField(required=False)
    tenant_id = serializers.CharField(required=False)
    tenant_name = serializers.CharField(required=False)
    cidr = serializers.CharField(required=False)
    vlan_id = serializers.IntegerField(required=False)
    ip = serializers.CharField(required=False)
    network_id = serializers.CharField(required=False)
    status = serializers.BooleanField(required=False)
    nfs_id = serializers.IntegerField(required=False)
    quota_id = serializers.CharField(required=False)
    region = serializers.CharField(required=False)
    file_agreement = serializers.CharField(required=False)
    file_size = serializers.CharField(required=False)

    class Meta:
        model = NFS
        fields = '__all__'


class UpdateNFSSerializer(serializers.ModelSerializer):
    name = serializers.CharField(required=False)

    class Meta:
        model = NFS
        fields = (
            'name'
        )
