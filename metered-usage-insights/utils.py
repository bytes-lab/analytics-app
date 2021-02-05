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


def get_weight_metric(tenant_id, unweighted_metric, weighted_metric, resource_type=None, start=None, end=None):
    unweighted = get_metric_value(tenant_id, unweighted_metric, resource_type, start, end)
    weighted = get_metric_value(tenant_id, weighted_metric, resource_type, start, end)
    _unweighted = unweighted['data']['result'][0]['value'][0]
    _weighted = weighted['data']['result'][0]['value'][0]

    return _unweighted, _weighted


def get_breakdown_resource_tier(start_date, end_date):
    tenants = get_tenants()
    metric_names = get_metric_names()
    resp = {}

    for metric_name, types in metric_names.items():
        resp[metric_name] = { 'unweighted': 0, 'weighted': 0 }

        for tenant in tenants:
            tenant_id = tenant['tenantId']
            _unweighted, _weighted = get_weight_metric(tenant_id, types['unweighted'], types['weighted'], None, start_date, end_date)
            resp[metric_name]['unweighted'] += _unweighted
            resp[metric_name]['weighted'] += _weighted

    return resp


def get_breakdown_client(start_date, end_date):
    tenants = get_tenants()
    metric_names = get_metric_names()
    resp = {}

    for tenant in tenants:
        tenant_id = tenant['tenantId']
        resp[tenant_id] = { 'name': tenant['tenantName'], 'unweighted': 0, 'weighted': 0 }

        for metric_name, types in metric_names.items():
            _unweighted, _weighted = get_weight_metric(tenant_id, types['unweighted'], types['weighted'], None, start_date, end_date)
            resp[tenant_id]['unweighted'] += _unweighted
            resp[tenant_id]['weighted'] += _weighted

    return resp
