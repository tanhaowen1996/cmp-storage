from django.contrib.postgres.indexes import BrinIndex
from django.db import models
from django.utils.translation import gettext_lazy as _


class NFS(models.Model):
    id = models.CharField(
        primary_key=True,
        editable=False,
        max_length=8,
        verbose_name=_('nfs id')
    )
    name = models.CharField(
        null=True,
        max_length=128
    )
    subnet_id = models.CharField(
        null=True,
        max_length=36
    )
    tenant_id = models.CharField(
        null=True,
        max_length=36
    )
    cidr = models.CharField(
        null=True,
        max_length=36
    )
    vlan_id = models.IntegerField(
        null=True
    )
    ip = models.CharField(
        null=True,
        max_length=36
    )
    network_id = models.CharField(
        null=True,
        max_length=36
    )
    status = models.CharField(
        null=True,
        max_length=36
    )
    nfs_id = models.IntegerField(
        null=True
    )
    quota_id = models.CharField(
        null=True,
        max_length=36
    )
    updated_at = models.DateTimeField(
        auto_now=True,
        verbose_name=_('updated time'))
    created_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name=_('created time'))

    class Meta:
        indexes = (BrinIndex(fields=['updated_at', 'created_at']),)

    def get_cidr(os_conn, network_id):
        import pdb
        pdb.set_trace()
        network = os_conn.network.get_network(network_id)
        os_port = os_conn.network.create_port(
            network_id=network.id,
            description="Used by LodeBalance VIP",
            name="LoadBalance_VIP"
        )
        os_conn.network.set_tags(
            os_port,
            tags=["vip"]
        )
        return os_port