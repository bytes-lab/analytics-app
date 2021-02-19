import os

import flask
import requests
import requests_cache

# requests_cache.install_cache('opsramp_cache', backend='sqlite', expire_after=3600*300, allowable_methods=("GET", "POST"))

BASE_URL = os.getenv('API_SERVER', '')


def get_msp_id():
    url = BASE_URL + '/msps.json?_ajax=true'
    res = requests.get(url, cookies=flask.request.cookies)

    if res.status_code == 200 and 'login_password' not in res.text:
        if res.json()['success']:
            return res.json()['mspId']


def get_clients_count():
    total_clients = '-'
    msp_id = get_msp_id()
    if msp_id:
        url = BASE_URL + f'/api/v2/tenants/msp_{msp_id}/clients/search'
        res = requests.get(url, cookies=flask.request.cookies)
        if res.status_code == 200:
            total_clients = res.json()['totalResults']

    return total_clients


def get_resources_count():
    total_resources = '-'
    msp_id = get_msp_id()
    if msp_id:
        url = BASE_URL + f'/api/v2/tenants/msp_{msp_id}/resources/search'
        res = requests.get(url, cookies=flask.request.cookies)
        if res.status_code == 200:
            total_resources = res.json()['totalResults']

    return total_resources
