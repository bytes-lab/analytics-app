import os
import json
import time

import flask
import requests

from dash.dependencies import Input, Output, State

BASE_URL = os.getenv('API_SERVER', '')


PLATFORM_ROUTE = os.getenv("PLATFORM_ROUTE", '')
in_store_id = "_oap_data_in_" + PLATFORM_ROUTE
out_store_id = "_oap_data_out_" + PLATFORM_ROUTE

def register_callbacks(app):
    # api integration
    @app.callback(
        Output('total_clients', 'children'),
        Input(out_store_id, 'data')
    )
    def get_total_clients(data):
        url = BASE_URL + '/msp_21998/clients/search'
        res = requests.get(url, verify=False, cookies=flask.request.cookies)
        total_clients = '-'
        if res.status_code == 200:
            total_clients = res.json()['totalResults']

        return total_clients

    @app.callback(
        Output('total_resources', 'children'),
        Input(out_store_id, 'data')
    )
    def get_total_resources(data):
        url = BASE_URL + '/msp_21998/resources/search'
        res = requests.get(url, verify=False, cookies=flask.request.cookies)
        total_resources = '-'
        if res.status_code == 200:
            total_resources = res.json()['totalResults']

        return total_resources
