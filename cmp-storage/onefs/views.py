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

    # def list(self, request, *args, **kwargs):
    #     try:
    #         pass
    #     except Exception as e:
    #         pass

    def create(self, request, *args, **kwargs):
        try:
            serializer = self.get_serializer(data=request.data)
            serializer.is_valid(raise_exception=True)
            data = serializer.validated_data
            cidr = NFS.get_cidr(request.os_conn, data.get('network_id'))
        except Exception as e:
            logger.error(f"try creating NFS ERROR: {e}")
            return Response({
                "detail": f"{e}"

            }, status=status.HTTP_400_BAD_REQUEST)

