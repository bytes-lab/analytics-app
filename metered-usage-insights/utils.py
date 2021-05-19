import os
import json

import flask
import requests
import requests_cache

requests_cache.install_cache('opsramp_cache', backend='sqlite', expire_after=3600*300, allowable_methods=("GET", "POST"))

BASE_URL = os.getenv('API_SERVER', '')


def get_tenants():
    url = BASE_URL + '/metricsql/tenants'
    res = requests.get(url)
    res.raise_for_status()

    return res.json()


def get_resource_types():
    url = BASE_URL + '/metricsql/resource-types'
    res = requests.get(url)
    res.raise_for_status()

    return res.json()


def get_metric_names():
    url = BASE_URL + '/metricsql/metric-names'
    res = requests.get(url)
    res.raise_for_status()

    return res.json()


def get_metric_value(tenant_id, metric_name, function, resource_type=None, start=None, end=None):
    url = BASE_URL + '/metricql/query'

    body = {
        "tenantId": tenant_id,
        "metricName": metric_name,
        "resourceType": resource_type,
        "function": function,
        "start": start,
        "end": end
    }

    res = requests.post(url, data=json.dumps(body))
    res.raise_for_status()

    return res.json()


def get_weight_metric(tenant_id, unweighted_metric, weighted_metric, function, resource_type=None, start=None, end=None):
    unweighted = get_metric_value(tenant_id, unweighted_metric, function, resource_type, start, end)
    weighted = get_metric_value(tenant_id, weighted_metric, function, resource_type, start, end)
    _unweighted = unweighted['data']['result'][0]['values']
    _weighted = weighted['data']['result'][0]['values']

    if function == "avg_over_time":
        return _unweighted[0], _weighted[0]
    else:
        return _unweighted, _weighted


def get_breakdown_resource_tier(start_date, end_date):
    tenants = get_tenants()
    metric_names = get_metric_names()
    resp = {}

    for metric_name, types in metric_names.items():
        resp[metric_name] = { 'unweighted': 0, 'weighted': 0 }

        for tenant in tenants:
            tenant_id = tenant['tenantId']
            _unweighted, _weighted = get_weight_metric(tenant_id, types['unweighted'], types['weighted'], "avg_over_time", None, start_date, end_date)
            resp[metric_name]['unweighted'] += _unweighted
            resp[metric_name]['weighted'] += _weighted

    return resp


def get_breakdown_time(start_date, end_date):
    tenants = get_tenants()
    metric_names = get_metric_names()
    resp = {}

    for metric_name, types in metric_names.items():
        for tenant in tenants:
            tenant_id = tenant['tenantId']
            weighted = get_metric_value(tenant_id, types['weighted'], "raw", None, start_date, end_date)
            values = weighted['data']['result'][0]['values']

            for value in values:
                if value[0] in resp:  # EPOC
                    resp[value[0]] += value[1]
                else:
                    resp[value[0]] = 0

    return resp


def get_breakdown_client(start_date, end_date):
    tenants = get_tenants()
    metric_names = get_metric_names()
    resp = {}

    for tenant in tenants:
        tenant_id = tenant['tenantId']
        resp[tenant_id] = { 'name': tenant['tenantName'], 'unweighted': 0, 'weighted': 0 }

        for metric_name, types in metric_names.items():
            _unweighted, _weighted = get_weight_metric(tenant_id, types['unweighted'], types['weighted'], "avg_over_time", None, start_date, end_date)
            resp[tenant_id]['unweighted'] += _unweighted
            resp[tenant_id]['weighted'] += _weighted

    return resp


def get_breakdown_resource_type(start_date, end_date):
    tenants = get_tenants()
    metric_names = get_metric_names()
    resource_types = get_resource_types()
    resp = {}

    for resource_type in resource_types:
        resp[resource_type] = { 'name': resource_type, 'unweighted': 0, 'weighted': 0 }

        for metric_name, types in metric_names.items():
            for tenant in tenants:
                tenant_id = tenant['tenantId']
                _unweighted, _weighted = get_weight_metric(tenant_id, types['unweighted'], types['weighted'], "avg_over_time", resource_type, start_date, end_date)
                resp[resource_type]['unweighted'] += _unweighted
                resp[resource_type]['weighted'] += _weighted

    return resp


def compute():
    data = flask.request.get_json()
    start_date = data.get('start_date', None)
    end_date = data.get('end_date', None)

    resp = {
        'tenants': get_tenants(),
        'resource_types': get_resource_types(),
        'breakdown_resource_type': get_breakdown_resource_type(start_date, end_date),
        'breakdown_client': get_breakdown_client(start_date, end_date),
        'breakdown_time': get_breakdown_time(start_date, end_date),
        'breakdown_resource_tier': get_breakdown_resource_tier(start_date, end_date),
    }

    return resp
