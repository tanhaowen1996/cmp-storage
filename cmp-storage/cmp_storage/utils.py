from django.conf import settings
import openstack
import logging

openstack.enable_logging(debug=settings.DEBUG)
logger = logging.getLogger(__package__)


class OpenstackMixin:

    @staticmethod
    def get_conn():
        return openstack.connect()
