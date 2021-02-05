import os
import json

import requests
import requests_cache

requests_cache.install_cache('opsramp_cache', backend='sqlite', expire_after=3600*30, allowable_methods=("GET", "POST"))

BASE_URL = os.getenv('API_SERVER', '')


def get_tenants():
    url = BASE_URL + '/metricsql/tenants'
    res = requests.get(url).json()

    return res


def get_resource_types():
    url = BASE_URL + '/metricsql/resource-types'
    res = requests.get(url).json()

    return res


def get_metric_names():
    url = BASE_URL + '/metricsql/metric-names'
    res = requests.get(url).json()

    return res


def get_metric_value(tenant_id, metric_name, resource_type=None, start=None, end=None):
    url = BASE_URL + '/metricql/query'

    body = {
        "tenantId": tenant_id,
        "metricName": metric_name,
        "resourceType": resource_type,
        "start": start,
        "end": end
    }

    res = requests.post(url, data=json.dumps(body)).json()

    return res
