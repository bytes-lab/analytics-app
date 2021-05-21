import flask
import requests_cache

# requests_cache.install_cache('opsramp_cache', backend='sqlite', expire_after=3600*300, allowable_methods=("GET", "POST"))

from analytics_sdk.utilities import (
    BASE_API_URL,
    get_msp_id,
    call_get_requests
)

def get_tenants():
    msp_id = get_msp_id()
    url = BASE_API_URL + f'/api/v2/tenants/{msp_id}/clients/minimal'
    res = call_get_requests(url, verify=False)
    
    if not res.ok:
        return []

    return res.json()


def get_resource_types():
    tenants = get_tenants()
    resource_types = []

    for tenant in tenants:
        tenant_id = tenant['uniqueId']
        url = BASE_API_URL + f'/metricsql/api/v7/tenants/{tenant_id}/metrics/label/resourceType/values'
        res = call_get_requests(url, verify=False)

        if not res.ok:
            continue

        resource_types += res.json()['data']
    
    return list(set(resource_types))


def get_metric_names():
    metric_names = {
        "inventoryOnly": {
            "unweighted": "usage_resource_InventoryOnly_unweighted",
            "weighted": "usage_resource_InventoryOnly_weighted"
        },
        "eventsOnly": {
            "unweighted": "usage_resource_EventsOnly_unweighted",
            "weighted": "usage_resource_EventsOnly_weighted"
        },
        "upDownOnly": {
            "unweighted": "usage_resource_UpDownOnly_unweighted",
            "weighted": "usage_resource_UpDownOnly_weighted"
        },
        "fullyManaged": {
            "unweighted": "usage_resource_FullyManaged_unweighted",
            "weighted": "usage_resource_FullyManaged_weighted"
        }
    }

    return metric_names


def get_metric_value(tenant_id, metric_name, function, resource_type=None, start=None, end=None):
    url = BASE_API_URL + f'/metricsql/api/v7/tenants/{tenant_id}/metrics'
    metric = f'{metric_name}{{resourceType="{resource_type}"}}' if resource_type else metric_name
    metric = f'{function}({metric})' if function else metric

    params = {
        "query": metric,
        "start": 1613887988,  # start,
        "end": 1621509199,  # end
        "encode": "true"  # optional
    }

    res = call_get_requests(url, params, verify=False)

    if not res.ok:
        return {"status": "fail"}

    return res.json()


def get_weight_metric(tenant_id, unweighted_metric, weighted_metric, function, resource_type=None, start=None, end=None):
    unweighted = get_metric_value(tenant_id, unweighted_metric, function, resource_type, start, end)
    weighted = get_metric_value(tenant_id, weighted_metric, function, resource_type, start, end)

    _unweighted = []
    _weighted = []

    if unweighted['status'] == 'success' and unweighted['data']['result']:
        _unweighted = unweighted['data']['result'][0]['values']

    if weighted['status'] == 'success' and weighted['data']['result']:
        _weighted = weighted['data']['result'][0]['values']

    if function == "avg":
        return sum([float(ii[1]) for ii in _unweighted]), sum([float(ii[1]) for ii in _weighted])
    else:
        return _unweighted, _weighted


def get_breakdown_resource_tier(start_date, end_date):
    tenants = get_tenants()
    metric_names = get_metric_names()
    resp = {}

    for metric_name, types in metric_names.items():
        resp[metric_name] = { 'unweighted': 0, 'weighted': 0 }

        for tenant in tenants:
            tenant_id = tenant['uniqueId']
            _unweighted, _weighted = get_weight_metric(tenant_id, types['unweighted'], types['weighted'], "avg", None, start_date, end_date)
            resp[metric_name]['unweighted'] += _unweighted
            resp[metric_name]['weighted'] += _weighted

    return resp


def get_breakdown_time(start_date, end_date):
    tenants = get_tenants()
    metric_names = get_metric_names()
    resp = {}

    for metric_name, types in metric_names.items():
        for tenant in tenants:
            tenant_id = tenant['uniqueId']
            weighted = get_metric_value(tenant_id, types['weighted'], "", None, start_date, end_date)
            if weighted['status'] == 'success' and weighted['data']['result']:
                values = weighted['data']['result'][0]['values']

                for value in values:
                    if value[0] in resp:  # EPOC
                        resp[value[0]] += float(value[1])
                    else:
                        resp[value[0]] = float(value[1])

    return resp


def get_breakdown_client(start_date, end_date):
    tenants = get_tenants()
    metric_names = get_metric_names()
    resp = {}

    for tenant in tenants:
        tenant_id = tenant['uniqueId']
        resp[tenant_id] = { 'name': tenant['name'], 'unweighted': 0, 'weighted': 0 }

        for metric_name, types in metric_names.items():
            _unweighted, _weighted = get_weight_metric(tenant_id, types['unweighted'], types['weighted'], "avg", None, start_date, end_date)
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
                tenant_id = tenant['uniqueId']
                _unweighted, _weighted = get_weight_metric(tenant_id, types['unweighted'], types['weighted'], "avg", resource_type, start_date, end_date)
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
