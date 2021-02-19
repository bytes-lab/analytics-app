import os
import json
import time

import flask

from dash.dependencies import Input, Output, State


from utils import *
from pages.utils import *


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
        tenants = get_tenants()
        return len(tenants)

    @app.callback(
        Output('total_resources', 'children'),
        Input(out_store_id, 'data')
    )
    def get_total_resources(data):
        resource_types = get_resource_types()
        return len(resource_types)
