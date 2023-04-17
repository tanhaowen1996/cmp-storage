import requests
from requests import exceptions
import urllib3
from onefs.session import OneFSMixin
import json
from urllib3.exceptions import InsecureRequestWarning
from cmp_storage.settings import ONEFS_URL, NFS_ROOT

nfs_conn = OneFSMixin.get_session()
urllib3.disable_warnings(InsecureRequestWarning)


def check_path(path):
    url = ONEFS_URL + "namespace" + NFS_ROOT + path
    try:
        response = requests.get(url=url, auth=nfs_conn,  verify=False)
        if response.status_code == 404:
            return False
        else:
            return True
    except exceptions.Timeout as e:
        print(e)
    except exceptions.HTTPError as e:
        print(e)


def add_path(path):
    url = ONEFS_URL + "namespace" + NFS_ROOT + path + "?overwrite=false"
    url_acl = ONEFS_URL + "namespace" + NFS_ROOT + path + "?acl"
    headers = {
        'x-isi-ifs-target-type': 'container'
    }
    payload_acl = json.dumps({
        "authoritative": "mode",
        "mode": "0777"
    })
    try:
        requests.put(url=url, headers=headers, auth=nfs_conn, verify=False)
        requests.put(url=url_acl, headers=headers, auth=nfs_conn, data=payload_acl, verify=False)
    except exceptions.Timeout as e:
        print(e)
    except exceptions.HTTPError as e:
        print(e)
    else:
        return True


def del_path(path):
    url = ONEFS_URL + "namespace" + NFS_ROOT + path + "?recursive=true"
    try:
        requests.delete(url=url, auth=nfs_conn, verify=False)
    except exceptions.Timeout as e:
        print(e)
    except exceptions.HTTPError as e:
        print(e)


def add_nfs(path, cidrs):
    url = ONEFS_URL + "platform/4/protocols/nfs/exports"
    path = NFS_ROOT + path
    payload = json.dumps({
        "paths": [path],
        "clients": cidrs
    })
    try:
        response = requests.post(url=url, auth=nfs_conn, data=payload, verify=False)
    except exceptions.Timeout as e:
        print(e)
    except exceptions.HTTPError as e:
        print(e)
    else:
        return response.json().get("id")


def del_nfs(id):
    url = ONEFS_URL + "platform/4/protocols/nfs/exports/" + str(id)
    try:
        response = requests.delete(url=url, auth=nfs_conn, verify=False)
        if response.status_code == 401:
            return del_nfs(id=id)
        else:
            return True
    except exceptions.Timeout as e:
        print(e)
    except exceptions.HTTPError as e:
        print(e)


def add_aliases(path, aliases):
    url = ONEFS_URL + "platform/2/protocols/nfs/aliases"
    path = NFS_ROOT + path
    payload = json.dumps({
        "name": "/"+aliases,
        "path": path
    })
    try:
        requests.post(url=url, auth=nfs_conn, data=payload, verify=False)
    except exceptions.Timeout as e:
        print(e)
    except exceptions.HTTPError as e:
        print(e)


def del_aliases(aliases):
    url = ONEFS_URL + "platform/2/protocols/nfs/aliases/%2F" + aliases
    try:
        requests.delete(url=url, auth=nfs_conn, verify=False)
    except exceptions.Timeout as e:
        print(e)
    except exceptions.HTTPError as e:
        print(e)


def get_aliases(aliases):
    url = ONEFS_URL + "platform/2/protocols/nfs/aliases/%2F" + aliases + "?check=true"
    try:
        response = requests.get(url=url, auth=nfs_conn, verify=False)
    except exceptions.Timeout as e:
        print(e)
    except exceptions.HTTPError as e:
        print(e)
    else:
        return response.json().get('aliases')[0].get('health')


def add_quotas(path, hard):
    url = ONEFS_URL + "platform/1/quota/quotas"
    payload = json.dumps({
        "container": True,
        "force": False,
        "enforced": True,
        "include_snapshots": False,
        "path": NFS_ROOT + path,
        "thresholds": {
            "hard": hard
        },
        "thresholds_include_overhead": False,
        "type": "directory"
    })
    try:
        responese = requests.post(url=url, auth=nfs_conn, data=payload, verify=False)
    except exceptions.Timeout as e:
        print(e)
    except exceptions.HTTPError as e:
        print(e)
    else:
        return responese.json().get('id')


def update_quotas(quota_id, hard):
    url = ONEFS_URL + "platform/1/quota/quotas/" + str(quota_id)
    payload = json.dumps({
        "thresholds": {
            "hard": hard
        }
    })
    try:
        requests.put(url=url, auth=nfs_conn, data=payload, verify=False)
    except exceptions.Timeout as e:
        print(e)
    except exceptions.HTTPError as e:
        print(e)


def get_usage(quota_id):
    url = ONEFS_URL + "platform/1/quota/quotas/" + str(quota_id)
    try:
        responese = requests.get(url=url, auth=nfs_conn, verify=False)
    except exceptions.Timeout as e:
        print(e)
    except exceptions.HTTPError as e:
        print(e)
    else:
        usage = {
            "hard": responese.json().get("quotas")[0].get("thresholds").get("hard"),
            "usage": responese.json().get("quotas")[0].get("usage").get("logical")
        }
        return usage


def del_quotas(id):
    url = ONEFS_URL + "platform/1/quota/quotas/" + str(id)
    try:
        responese = requests.delete(url=url, auth=nfs_conn, verify=False)
        if responese.status_code == 200 or responese.status_code == 201 or responese.status_code == 204:
            return True
        if responese.status_code == 401:
            return del_quotas(id)
        if responese.status_code == 404:
            print("不存在 platform/1/quota/quotas/" + str(id))
            return True
    except exceptions.Timeout as e:
        print(e)
    except exceptions.HTTPError as e:
        print(e)
    return False
