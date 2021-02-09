import os
import json
import time

import flask
import plotly.graph_objs as go

from dash.dependencies import Input, Output, State
from analytics_sdk.utilities import (
    save_archive,
    get_archives,
    get_archive,
    generate_pdf
)

from utils import *
from pages.utils import *


PLATFORM_ROUTE = os.getenv("PLATFORM_ROUTE", '')
in_store_id = "_oap_data_in_" + PLATFORM_ROUTE
out_store_id = "_oap_data_out_" + PLATFORM_ROUTE
oap_name = os.getenv("PLATFORM_ROUTE", 'metered-usage-insight')

def register_callbacks(app):
    """ Common settings """

    # handle pdf
    @app.callback(
        # [
        #     Output("download-pdf", "children"),
        #     Output("download-pdf", "href")
        # ],
        Output('dummy-store', 'data'),
        Input('gen-pdf', 'n_clicks'),
        State(out_store_id, 'data')
    )
    def generate_report(n_clicks, data):
        if n_clicks:  # avoid initial loading
            print_route = '/full-view'
            res = generate_pdf(oap_name, data, 'A4', print_route)
            return res['Location'] 

    # handle archive
    @app.callback(
        [
            Output("list-archives", "options"),
            Output('list-archives', 'value'),
        ],
        Input('gen-archive', 'n_clicks'),
        State(out_store_id, 'data')
    )
    def create_archive(n_clicks, data):
        archive_id = None
        if n_clicks:
            print_route = '/full-view'
            archive_id = save_archive(oap_name, data, 'A4', print_route)['archive_id']

        archives = get_archives(oap_name)

        return archives, archive_id

    @app.callback(
        Output(in_store_id, "data"),
        Input('list-archives', 'value')
    )
    def load_archive(archive_id):
        if not archive_id:
            return

        archive = get_archive(archive_id)

        return json.loads(archive['state'])

    # save / load settings
    @app.callback(
        Output(out_store_id, "data"),
        [
            Input("reporting_priod_picker", "start_date"),
            Input("reporting_priod_picker", "end_date"),
        ]
    )
    def save_settings(start_date, end_date):
        return start_date, end_date

    @app.callback(
        Output("reporting_priod_picker", "start_date"),
        Output("reporting_priod_picker", "end_date"),
        Input(in_store_id, "data"),
    )
    def load_settings(data):
        return data if data else [None, None]

    # pie charts

    pie_graph_layout = dict(
        autosize=True,
        automargin=True,
        height=150,
        margin=dict(l=30, r=30, b=00, t=00),
        hovermode="closest",
        plot_bgcolor="#F9F9F9",
        paper_bgcolor="#fff",
        font=dict(color="#777777"),
        legend=dict(
            font=dict(color="#333", size="10"),
            orientation="v",
            bgcolor="rgba(0,0,0,0)",
            y=0.8),
        title=""
    )

    pie_graph_data = dict(
        type="pie",
        hoverinfo="label+value+percent",
        textinfo="percent",
        textfont=dict(size=9, color="#fff"),
        hole=0.5,
        direction="clockwise",
        sort=False,
        marker=dict(
            colors=["#0077C8", "#32a3df", "#673ab7", "#9c27b0"],
            line=dict(color='#fff', width=1)
        ),
    )

    @app.callback(
        Output("pie-graph-total-usage", "figure"),
        [
            Input("reporting_priod_picker", "start_date"),
            Input("reporting_priod_picker", "end_date"),
        ]
    )
    def pie_graph_total_usage(start_date, end_date):
        breakdown_resource_tier = get_breakdown_resource_tier(start_date, end_date)

        x_values = []
        y_values = []

        for metric_name, values in breakdown_resource_tier.items():
            x_values.append(metric_name.title())
            y_values.append(values['unweighted']+values['weighted'])

        data = dict(pie_graph_data)
        data['labels'] = x_values
        data['values'] = y_values

        figure = dict(data=[data], layout=pie_graph_layout)

        return figure

    @app.callback(
        Output("pie-graph-unweighted-usage", "figure"),
        [
            Input("reporting_priod_picker", "start_date"),
            Input("reporting_priod_picker", "end_date"),
        ]
    )
    def pie_graph_unweighted_usage(start_date, end_date):
        breakdown_client = get_breakdown_client(start_date, end_date)
        clients = sorted(breakdown_client.values(), key=lambda k: -k['unweighted'])

        x_values = [ii['name'].title() for ii in clients[:4]] + ['Other']
        y_values = [ii['unweighted'] for ii in clients[:4]] + [sum([ii['unweighted'] for ii in clients[4:]])]

        data = dict(pie_graph_data)
        data['labels'] = x_values
        data['values'] = y_values

        figure = dict(data=[data], layout=pie_graph_layout)

        return figure

    @app.callback(
        Output("pie-graph-weighted-usage", "figure"),
        [
            Input("reporting_priod_picker", "start_date"),
            Input("reporting_priod_picker", "end_date"),
        ]
    )
    def pie_graph_weighted_usage(start_date, end_date):
        breakdown_client = get_breakdown_client(start_date, end_date)

        clients = sorted(breakdown_client.values(), key=lambda k: -k['weighted'])

        x_values = [ii['name'].title() for ii in clients[:4]] + ['Other']
        y_values = [ii['weighted'] for ii in clients[:4]] + [sum([ii['weighted'] for ii in clients[4:]])]

        data = dict(pie_graph_data)
        data['labels'] = x_values
        data['values'] = y_values

        figure = dict(data=[data], layout=pie_graph_layout)

        return figure

    # bar charts

    bar_graph_layout = dict(
        autosize=False,
        bargap=0.65,
        font={"family": "Raleway", "size": 10},
        height=200,
        hovermode="closest",
        legend={
            "x": -0.0228945952895,
            "y": -0.189563896463,
            "orientation": "h",
            "yanchor": "top"
        },
        margin={
            "r": 0,
            "t": 20,
            "b": 20,
            "l": 30
        },
        showlegend=False,
        title="",
        # width=330,
        xaxis={
            "autorange": True,
            "range": [-0.5, 4.5],
            "showline": True,
            "title": "",
            "type": "category"
        },
        yaxis={
            "autorange": True,
            "range": [0, 3200.9789473684],
            "showgrid": True,
            "showline": True,
            "title": "",
            "type": "linear",
            "zeroline": False
        }
    )

    bar_graph_data = dict(
        type="bar",
        marker={
            "color": "#0077c8",
            "line": {
                "color": "rgb(255, 255, 255)",
                "width": 2
            }
        }
    )

    @app.callback(
        Output("bar-graph-top-10-clients-weighted", "figure"),
        [
            Input("reporting_priod_picker", "start_date"),
            Input("reporting_priod_picker", "end_date"),
        ]
    )
    def bar_graph_top_10_clients_weighted(start_date, end_date):
        breakdown_client = get_breakdown_client(start_date, end_date)
        clients = sorted(breakdown_client.values(), key=lambda k: -k['weighted'])

        bar_data = dict(bar_graph_data)
        bar_data['x'] = [ii['name'].title() for ii in clients[:10]]
        bar_data['y'] = [ii['weighted'] for ii in clients[:10]]

        figure = {
            "data": [bar_data],
            "layout": bar_graph_layout,
        }

        return figure

    @app.callback(
        Output("bar-graph-bottom-10-clients-weighted", "figure"),
        [
            Input("reporting_priod_picker", "start_date"),
            Input("reporting_priod_picker", "end_date"),
        ]
    )
    def bar_graph_bottom_10_clients_weighted(start_date, end_date):
        breakdown_client = get_breakdown_client(start_date, end_date)
        clients = sorted(breakdown_client.values(), key=lambda k: k['weighted'])

        bar_data = dict(bar_graph_data)
        bar_data['x'] = [ii['name'].title() for ii in clients[:10]]
        bar_data['y'] = [ii['weighted'] for ii in clients[:10]]

        figure = {
            "data": [bar_data],
            "layout": bar_graph_layout,
        }

        return figure

    @app.callback(
        Output("pie-graph-unweighted-type-usage", "figure"),
        [
            Input("reporting_priod_picker", "start_date"),
            Input("reporting_priod_picker", "end_date"),
        ]
    )
    def pie_graph_unweighted_type_usage(start_date, end_date):
        breakdown_resource_type = get_breakdown_resource_type(start_date, end_date)
        resource_types = sorted(breakdown_resource_type.values(), key=lambda k: -k['unweighted'])

        x_values = [ii['name'].title() for ii in resource_types]
        y_values = [ii['unweighted'] for ii in resource_types]

        data = dict(pie_graph_data)
        data['labels'] = x_values
        data['values'] = y_values

        figure = dict(data=[data], layout=pie_graph_layout)

        return figure

    @app.callback(
        Output("bar-graph-top-10-resource-type-weighted", "figure"),
        [
            Input("reporting_priod_picker", "start_date"),
            Input("reporting_priod_picker", "end_date"),
        ]
    )
    def bar_graph_top_10_resource_type_weighted(start_date, end_date):
        breakdown_resource_type = get_breakdown_resource_type(start_date, end_date)
        resource_types = sorted(breakdown_resource_type.values(), key=lambda k: -k['weighted'])

        bar_data = dict(bar_graph_data)
        bar_data['x'] = [ii['name'].title() for ii in resource_types[:10]]
        bar_data['y'] = [ii['weighted'] for ii in resource_types[:10]]

        figure = {
            "data": [bar_data],
            "layout": bar_graph_layout,
        }

        return figure

    @app.callback(
        Output("bar-graph-bottom-10-resource-type-weighted", "figure"),
        [
            Input("reporting_priod_picker", "start_date"),
            Input("reporting_priod_picker", "end_date"),
        ]
    )
    def bar_graph_bottom_10_resource_type_weighted(start_date, end_date):
        breakdown_resource_type = get_breakdown_resource_type(start_date, end_date)
        resource_types = sorted(breakdown_resource_type.values(), key=lambda k: k['weighted'])

        bar_data = dict(bar_graph_data)
        bar_data['x'] = [ii['name'].title() for ii in resource_types[:10]]
        bar_data['y'] = [ii['weighted'] for ii in resource_types[:10]]

        figure = {
            "data": [bar_data],
            "layout": bar_graph_layout,
        }

        return figure

    @app.callback(
        Output("bar-graph-weighted-time", "figure"),
        [
            Input("reporting_priod_picker", "start_date"),
            Input("reporting_priod_picker", "end_date"),
        ]
    )
    def bar_graph_weighted_time(start_date, end_date):
        start_date = "2021-01-01T00:00:00.0Z"
        end_date = "2021-01-01T00:12:00.0Z"
        breakdown_time = get_breakdown_time(start_date, end_date)
        _breakdown_time = [(key, val) for key, val in breakdown_time.items()]
        _breakdown_time = sorted(_breakdown_time, key=lambda k: k[0])

        bar_data = dict(bar_graph_data)
        bar_data['x'] = [
            time.strftime('%H:%M', time.localtime(ii[0]))
            for ii in _breakdown_time[:12]
        ]
        bar_data['y'] = [ii[1] for ii in _breakdown_time[:12]]
        bar_data['type'] = 'scatter'

        figure = {
            "data": [bar_data],
            "layout": bar_graph_layout,
        }

        return figure

    @app.callback(
        Output("pie-graph-weighted-type-usage", "figure"),
        [
            Input("reporting_priod_picker", "start_date"),
            Input("reporting_priod_picker", "end_date"),
        ]
    )
    def pie_graph_weighted_type_usage(start_date, end_date):
        breakdown_resource_type = get_breakdown_resource_type(start_date, end_date)

        resource_types = sorted(breakdown_resource_type.values(), key=lambda k: -k['weighted'])

        x_values = [ii['name'].title() for ii in resource_types]
        y_values = [ii['weighted'] for ii in resource_types]

        data = dict(pie_graph_data)
        data['labels'] = x_values
        data['values'] = y_values

        figure = dict(data=[data], layout=pie_graph_layout)

        return figure

    @app.callback(
        Output("table-resource-type", "children"),
        [
            Input("reporting_priod_picker", "start_date"),
            Input("reporting_priod_picker", "end_date"),
        ]
    )
    def table_resource_type(start_date, end_date):
        breakdown_resource_tier = get_breakdown_resource_tier(start_date, end_date)
        table_rows = [['Resource Tier', 'Usage (Unweighted)', 'Usage (Weighted)']]

        total_unweighted = total_weighted = 0
        for metric_name, values in breakdown_resource_tier.items():
            table_rows.append([metric_name.title(), f'{values["unweighted"]:,.2f}', f'{values["weighted"]:,.2f}'])
            total_unweighted += values['unweighted']
            total_weighted += values['weighted']

        table_rows.append(['Total', f'{total_unweighted:,.2f}', f'{total_weighted:,.2f}'])

        return render_table(table_rows)

    # api integration
    @app.callback(
        Output('total_clients', 'children'),
        Input('gen-pdf', 'n_clicks'),
        State(out_store_id, 'data')
    )
    def get_total_clients(n_clicks, data):
        if not n_clicks:  # initial loading
            tenants = get_tenants()
            return len(tenants)

    @app.callback(
        Output('total_resources', 'children'),
        Input('gen-pdf', 'n_clicks'),
        State(out_store_id, 'data')
    )
    def get_total_resources(n_clicks, data):
        if not n_clicks:  # initial loading
            resource_types = get_resource_types()
            return len(resource_types)
