from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from .authentication import OSAuthentication
from .serializers import NFSSerializer, UpdateNFSSerializer
from .models import NFS
from .filters import NFSFilter
import logging
import ast

logger = logging.getLogger(__package__)


class OSCommonModelMixin:
    update_serializer_class = None

    def get_serializer_class(self):
        return {
            'PUT': self.update_serializer_class
        }.get(self.request.method, self.serializer_class)


class NFSViewSet(OSCommonModelMixin, viewsets.ModelViewSet):
    """
        list:
        Get NFS list

        create:
        Create NFS

        retrieve:
        Get NFS

        update:
        修改name

        destroy:
        drop NFS

        update_quota:
        修改文件系统容量
    """
    authentication_classes = (OSAuthentication,)
    filterset_class = NFSFilter
    serializer_class = NFSSerializer
    update_serializer_class = UpdateNFSSerializer
    queryset = NFS.objects.all().order_by('-created_at')

    def get_serializer_class(self):
        return NFSSerializer

    def get_queryset(self):
        qs = super().get_queryset()
        qs = qs.filter(region=self.request.headers.get("Region"))
        if not self.request.user.is_staff:
            qs = qs.filter(tenant_id=self.request.headers.get("ProjectId"))
        return qs

    def create(self, request, *args, **kwargs):
        try:
            serializer = self.get_serializer(data=request.data)
            serializer.is_valid(raise_exception=True)
            data = serializer.validated_data
            network_ids = ast.literal_eval(data.get('network_id'))
            cidrs, subnet_ids = NFS.get_cidr(request.os_conn, network_ids=network_ids)
            project_id = self.request.headers.get("ProjectId")
            id = NFS.get_id()
            ip = NFS.get_ip()
            vlan_id = int(cidrs[0].split(".")[2])
            while NFS.objects.filter(id=id):
                id = NFS.get_id()
            nfs, quota_id = NFS.create_nfs(project_id=project_id, path_id=id, cidrs=cidrs, file_size=data.get('file_size', 50))
            nfs_status = NFS.get_status(nfs_id=id)

        except Exception as e:
            logger.error(f"try creating NFS ERROR: {e}")
            return Response({
                "detail": f"{e}"

            }, status=status.HTTP_400_BAD_REQUEST)
        else:
            serializer.save(
                id=id,
                name=data['name'],
                subnet_id=subnet_ids,
                cidr=cidrs,
                tenant_id=request.tenant.get("id"),
                tenant_name=request.tenant.get("name"),
                network_id=network_ids,
                nfs_id=nfs,
                ip=ip,
                status=nfs_status,
                vlan_id=vlan_id,
                quota_id=quota_id,
                region=request.tenant.get("region_name"),
                file_size=data.get('file_size', 50),
                file_agreement=data['file_agreement'],
                created_user=self.request.user
            )
            headers = self.get_success_headers(serializer.data)
            return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)

    def list(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())

        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            data = []
            for nfs in serializer.data:
                usage = NFS.get_usage(quota_id=nfs.get('quota_id'))
                nfs_data = {
                    "cidr": ast.literal_eval(nfs.get('cidr')),
                    "createTime": nfs.get('created_at'),
                    "hard": usage.get('hard'),
                    "id": nfs.get('id'),
                    "ip": nfs.get('ip'),
                    "name": nfs.get('name'),
                    "path": str(nfs.get('ip')) + ":/" + nfs.get('id'),
                    "fileSize": nfs.get('file_size'),
                    "fileAgreement": nfs.get('file_agreement'),
                    "usageSize": usage.get('usage'),
                    "status": nfs.get('status'),
                    "tenantId": nfs.get('tenant_id'),
                    "tenantName": nfs.get('tenant_name'),
                    "createdUser": nfs.get('created_user')
                }
                data.append(nfs_data)
            return self.get_paginated_response(data)

        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        try:
            usage = NFS.get_usage(quota_id=instance.quota_id)
        except Exception as e:
            logger.error(f"try creating NFS ERROR: {e}")
            return Response({
                "detail": f"{e}"

            }, status=status.HTTP_400_BAD_REQUEST)
        else:
            data = {
                "cidr": ast.literal_eval(instance.cidr),
                "createTime": instance.created_at.now().strftime("%Y-%m-%d %H:%M:%S"),
                "hard": usage.get('hard'),
                "id": instance.id,
                "ip": instance.ip,
                "name": instance.name,
                "path": str(instance.ip) + ":/" + instance.id,
                "fileSize": instance.file_size,
                "fileAgreement": instance.file_agreement,
                "usageSize": usage.get('usage'),
                "status": instance.status,
                "tenantId": instance.tenant_id,
                "tenantName": instance.tenant_name,
                "createdUser": instance.created_user
            }
            return Response(data, status=status.HTTP_201_CREATED)

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        try:
            instance.delete_nfs(project_id=instance.tenant_id, id=instance.id, nfs_id=instance.nfs_id,
                                quota_id=instance.quota_id)
        except Exception as e:
            logger.error(f"try creating NFS ERROR: {e}")
            return Response({
                "detail": f"{e}"

            }, status=status.HTTP_400_BAD_REQUEST)
        else:
            self.perform_destroy(instance)
            return Response("删除成功", status=status.HTTP_201_CREATED)

    def update(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)

    @action(detail=True, methods=['post'])
    def update_quota(self, request, *args, **kwargs):
        instance = self.get_object()
        try:
            instance.update_quota(quota_id=instance.quota_id, quota=request.data.get('quota'))
        except Exception as e:
            logger.error(f"try creating NFS ERROR: {e}")
            return Response({
                "detail": f"{e}"

            }, status=status.HTTP_400_BAD_REQUEST)
        else:
            instance.file_size = request.data.get('quota')
            instance.save()
            return Response("更新成功", status=status.HTTP_201_CREATED)
