# from pprint import pprint
# import urllib3
# import isi_sdk_9_1_0
# from isi_sdk_9_1_0.rest import ApiException
#
# urllib3.disable_warnings()
# # configure username and password
# configuration = isi_sdk_9_1_0.Configuration()
# configuration.username = "admin"
# configuration.password = "admin"
# configuration.verify_ssl = False
# # configure host
# configuration.host = "https://10.1.51.203:8080"
# api_client = isi_sdk_9_1_0.ApiClient(configuration)
# protocols_api = isi_sdk_9_1_0.ProtocolsApi(api_client)
# # get all exports
# sort = "description"
# limit = 50
# dir = "ASC"
# protocols_api.create_nfs_export()
# try:
#     api_response = protocols_api.list_nfs_exports(sort=sort, limit=limit, dir=dir)
#     pprint(api_response)
# except ApiException as e:
#     print("Exception when calling ProtocolsApi->list_nfs_exports: %s" % e)

url1 = "https://10.1.51.203:8080/platform/2/protocols/nfs/exports"
url = "https://10.1.51.203:8080/namespace/ifs/thw22"
url2 = "https://10.1.51.203:8080/namespace/ifs/thw/test?overwrite=false"

from requests.auth import HTTPBasicAuth
import requests
from requests import exceptions
import json
import urllib3
from urllib3.exceptions import InsecureRequestWarning
rw_session = HTTPBasicAuth("admin", "admin")
urllib3.disable_warnings(InsecureRequestWarning)
headers = {
    'x-isi-ifs-target-type': 'container'
}
payload = json.dumps({
  "authoritative": "mode",
  "mode": "777",
})
try:
    r = requests.get(url=url, auth=rw_session, verify=False)
except exceptions.Timeout as e:
    print(e)
except exceptions.HTTPError as e:
    print(e)
if r.status_code == 404:
    print("sssss")
print(r.status_code)
# # r = requests.get(url, auth=rw_session, verify=False)
# response_dict = r.json()
#     try:
#         VServers = response_dict.get("SlbNewCfgEnhVirtServerTable")