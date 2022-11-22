from django.contrib.postgres.indexes import BrinIndex
from django.db import models
from django.utils.translation import gettext_lazy as _
from onefs import client as nfs_client


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
    region = models.CharField(
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
        network = os_conn.network.get_network(network_id)
        subnet_id = network.subnet_ids[0]
        cidr = os_conn.network.get_subnet(subnet_id).cidr
        return cidr, subnet_id

    def get_id():
        import uuid
        array = ["0", "1", "2", "3", "4", "5", "6", "7", "8", "9",
                 "a", "b", "c", "d", "e", "f", "g", "h", "i", "j",
                 "k", "l", "m", "n", "o", "p", "q", "r", "s", "t",
                 "u", "v", "w", "x", "y", "z"]

        id = str(uuid.uuid4()).replace("-", "")
        buffer = []

        for i in range(0, 8):
            start = i * 4
            end = i * 4 + 4
            val = int(id[start:end], 16)
            buffer.append(array[val % 36])
        return "".join(buffer)

    def create_nfs(project_id, path_id, cidr):
        if not nfs_client.check_path(path=project_id):
           nfs_client.add_path(path=project_id)
        path = project_id + "/" + path_id
        if not nfs_client.check_path(path=path):
            nfs_client.add_path(path=path)
        nfs = nfs_client.add_nfs(path=path, cidr=cidr)
        nfs_client.add_aliases(path=path, aliases=path_id)
        quota_id = nfs_client.add_quotas(path=path, hard=536870912000)
        return nfs, quota_id

    def delete_nfs(self, project_id, id, nfs_id, quota_id):
        nfs_client.del_quotas(id=quota_id)
        nfs_client.del_aliases(aliases=id)
        path = project_id + "/" + id
        if nfs_client.del_nfs(id=nfs_id):
            nfs_client.del_path(path=path)

    def update_quota(self, quota_id, quota):
        nfs_client.update_quotas(quota_id=quota_id, hard=int(quota)*1024*1024*1024)
