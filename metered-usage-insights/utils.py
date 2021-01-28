import json

import requests

NODE_IP = '3.101.123.155'
NODE_PORT = '8000'

def get_resource_types(client_id=None):
    url = f'http://{NODE_IP}:{NODE_PORT}/metricsql/resource-types'
    res = requests.get(url).json()

    return res


def get_metric_types(client_id=None):
    url = f'http://{NODE_IP}:{NODE_PORT}/metricsql/metric-types'
    res = requests.get(url).json()

    return res


def get_metric_value(metric, start=None, end=None):
    url = f'http://{NODE_IP}:{NODE_PORT}/metricql/query'
    body = {
        "metric": metric,
        "start": start,
        "end": end
    }

    res = requests.post(url, data=json.dumps(body)).json()

    return res
