import os
import flask
import requests

APP_SERVICE_BASE_URL = os.getenv('APP_SERVICE_BASE_URL', '')


def get_run_result(run_id):
    print(run_id, '*'*20)
    if run_id:
        result = flask.session.get(run_id)
        if not result:
            url = APP_SERVICE_BASE_URL + f'/api/v1/analysis-runs/{run_id}/'
            analysis_run = requests.get(url).json()
            result = analysis_run['result']
    else:
        analysis_id = 'ba566d3c-6fae-4c3f-9803-8e2ceb8b3c04'
        url = APP_SERVICE_BASE_URL + f'/api/v1/analysis-runs/latest/?anaysis={analysis_id}'
        analysis_run = requests.get(url).json()

        if analysis_run:
            result = analysis_run['result']
        else:
            result = {}

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
