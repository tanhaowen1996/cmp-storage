from requests.auth import HTTPBasicAuth
from cmp_storage.settings import ONEFS_USER, ONEFS_URL, ONEFS_PASSWORD


class OneFSMixin:

    @staticmethod
    def get_session():
        nfs_session = HTTPBasicAuth(ONEFS_USER, ONEFS_PASSWORD)
        return nfs_session