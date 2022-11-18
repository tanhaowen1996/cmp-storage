from django.conf import settings
from django.contrib.auth.models import User
from rest_framework import (
    authentication,
    exceptions
)
from keystoneauth1 import session
from keystoneauth1.identity import v3
from cmp_storage.utils import openstack
import logging

logger = logging.getLogger(__package__)


class OSAuthentication(authentication.BaseAuthentication):
    OS_TOKEN_KEY = settings.OS_TOKEN_KEY

    def authenticate(self, request):
        try:
            if self.OS_TOKEN_KEY not in request.headers:
                raise KeyError(f"{self.OS_TOKEN_KEY} is missing")

            os_auth = v3.Token(
                auth_url=settings.OS_AUTH_URL,
                token=request.headers[self.OS_TOKEN_KEY],
                project_id=request.headers.get("ProjectId"),
                project_domain_name=settings.OS_PROJECT_DOMAIN_NAME,
            )
            request.os_conn = openstack.connection.Connection(
                session=session.Session(auth=os_auth),
                identity_api_version=settings.OS_IDENTITY_API_VERSION,
                interface=settings.OS_INTERFACE,
                region_name=request.headers.get("Region"),
            )
        except Exception as exc:
            msg = f"invalid request header: {exc}"
            logger.error(msg)
            raise exceptions.AuthenticationFailed(msg)
        else:
            user_id = os_auth.get_user_id(session=session.Session(auth=os_auth))
            users = request.os_conn.get_user(user_id)
            projects = request.os_conn.get_project(request.headers.get("ProjectId"))
            user, created = User.objects.update_or_create(
                defaults={
                    'username': users.get("name"),
                    'is_staff': bool(int(request.headers.get("IsPlatform")))
                })
            request.tenant = {
                'id': projects.get('id'),
                'name': projects.get('name'),
                'region_name': request.headers.get("Region")
            }
            return (user, None)
