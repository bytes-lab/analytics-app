import json

import requests
import requests_cache

requests_cache.install_cache('opsramp_cache', backend='sqlite', expire_after=300)
BASE_URL = 'http://don-mk8s-lb-3c9b790ca6219e7e.elb.us-west-1.amazonaws.com'


def get_tenants(client_id=None):
    url = BASE_URL + '/metricsql/tenants'
    res = requests.get(url).json()

    return res


def get_resource_types(client_id=None):
    url = BASE_URL + '/metricsql/resource-types'
    res = requests.get(url).json()

    return res


def get_metric_types(client_id=None):
    url = BASE_URL + '/metricsql/metric-names'
    res = requests.get(url).json()

    return res


def get_metric_value(tenant_id, metric_name, start=None, end=None):
    print (tenant_id, metric_name, start, end, 12345)
    url = BASE_URL + '/metricql/query'
    body = {
        "tenantId": tenant_id,
        "metricName": metric_name,
        "start": start,
        "end": end
    }

    res = requests.post(url, data=json.dumps(body)).json()

    return res
