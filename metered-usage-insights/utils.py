import os
import json

import flask
import requests

APP_SERVICE_BASE_URL = os.getenv('APP_SERVICE_BASE_URL', '')


def get_run_result(run_id):
    print(run_id, 111)

    def _get_run_result(url):
        resp = requests.get(url)
        analysis_run = resp.json()

        if resp.ok and analysis_run:
            flask.session[run_id] = analysis_run['result']  # str
            result = json.loads(analysis_run['result'])
        else:
            result = {}
        
        return result
        
    if run_id:
        str_result = flask.session.get(run_id)
        if str_result:
            result = json.loads(str_result)
        else:
            url = APP_SERVICE_BASE_URL + f'/api/v1/analysis-runs/{run_id}/'
            result = _get_run_result(url)
    else:
        analysis_id = 'ba566d3c-6fae-4c3f-9803-8e2ceb8b3c04'
        url = APP_SERVICE_BASE_URL + f'/api/v1/analysis-runs/latest/?analysis={analysis_id}'
        result = _get_run_result(url)

    return result


def get_tenants(run_id):
    run_result = get_run_result(run_id)
    return run_result.get('tenants', [])


def get_resource_types(run_id):
    run_result = get_run_result(run_id)
    return run_result.get('resource_types', [])


def get_breakdown_resource_type(run_id):
    run_result = get_run_result(run_id)
    return run_result.get('breakdown_resource_type', {})


def get_breakdown_client(run_id):
    run_result = get_run_result(run_id)
    return run_result.get('breakdown_client', {})


def get_breakdown_time(run_id):
    run_result = get_run_result(run_id)
    return run_result.get('breakdown_time', {})


def get_breakdown_resource_tier(run_id):
    run_result = get_run_result(run_id)
    return run_result.get('breakdown_resource_tier', {})
