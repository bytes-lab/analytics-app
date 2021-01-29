import json

import requests

BASE_URL = 'http://don-mk8s-lb-3c9b790ca6219e7e.elb.us-west-1.amazonaws.com'


def get_resource_types(client_id=None):
    url = BASE_URL + '/metricsql/resource-types'
    res = requests.get(url).json()

    return res


def get_metric_types(client_id=None):
    url = BASE_URL + '/metricsql/metric-types'
    res = requests.get(url).json()

    return res


def get_metric_value(metric, start=None, end=None):
    url = BASE_URL + '/metricql/query'
    body = {
        "metric": metric,
        "start": start,
        "end": end
    }

    res = requests.post(url, data=json.dumps(body)).json()

    return res
