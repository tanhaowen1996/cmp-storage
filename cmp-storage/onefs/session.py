from requests.auth import HTTPBasicAuth
import isi_sdk_9_1_0
from cmp_storage.settings import ONEFS_USER, ONEFS_URL, ONEFS_PASSWORD


class OneFSMixin:

    @staticmethod
    def get_session():
        nfs_session = HTTPBasicAuth(ONEFS_USER, ONEFS_PASSWORD)
        return nfs_session
        # configuration = isi_sdk_9_1_0.Configuration()
        # configuration.username = ONEFS_USER
        # configuration.password = ONEFS_PASSWORD
        # configuration.verify_ssl = False
        # # configure host
        # configuration.host = ONEFS_URL
        # api_client = isi_sdk_9_1_0.ApiClient(configuration)
        # return api_client