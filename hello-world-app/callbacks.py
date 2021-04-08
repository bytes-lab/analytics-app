import os

from dash.dependencies import Input, Output, State

from utils import *

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
        total_clients = get_clients_count()

        return total_clients

    @app.callback(
        Output('total_resources', 'children'),
        Input(out_store_id, 'data')
    )
    def get_total_resources(data):
        total_resources = get_resources_count()

        return total_resources

    @app.callback(
        Output('report-start-date', 'children'),
        Input('op-filter-start-date', 'data')
    )
    def get_filter_start_date(date):
        print (date, 123)
        return date

    @app.callback(
        Output('report-end-date', 'children'),
        Input('op-filter-end-date', 'data')
    )
    def get_filter_end_date(date):
        print (date, 456)
        return date
