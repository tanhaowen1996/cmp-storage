from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from .authentication import OSAuthentication
from .serializers import NFSSerializer
from .models import NFS
from .filters import NFSFilter
from requests import exceptions
import logging
import openstack

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
        修改name和描述

        destroy:
        drop NFS
    """
    authentication_classes = (OSAuthentication,)
    filterset_class = NFSFilter
    serializer_class = NFSSerializer
    queryset = NFS.objects.all().order_by('-created_at')

    def get_serializer_class(self):
        return NFSSerializer

    def get_queryset(self):
        qs = super().get_queryset()
        qs = qs.filter(provider=self.request.headers.get("Region"))
        if not self.request.user.is_staff:
            qs = qs.filter(tenant_id=self.request.headers.get("ProjectId"))
        return qs

    def create(self, request, *args, **kwargs):
        try:
            serializer = self.get_serializer(data=request.data)
            serializer.is_valid(raise_exception=True)
            data = serializer.validated_data
            cidr, subnet_id = NFS.get_cidr(request.os_conn, data.get('network_id'))
            project_id = self.request.headers.get("ProjectId")
            id = NFS.get_id()
            while NFS.objects.filter(id=id):
                id = NFS.get_id()
            nfs = NFS.create_nfs(project_id=project_id, path_id=id, cidr=cidr, name=data['name'])

        except Exception as e:
            logger.error(f"try creating NFS ERROR: {e}")
            return Response({
                "detail": f"{e}"

            }, status=status.HTTP_400_BAD_REQUEST)
        else:
            serializer.save(
                id=id,
                name=data['name'],
                subnet_id=subnet_id,
                cidr=cidr,
                tenant_id=request.tenant.get("id"),
                network_id=data.get('network_id'),
                nfs_id=nfs,
                region=request.tenant.get("region_name")
            )
            headers = self.get_success_headers(serializer.data)
            return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)

