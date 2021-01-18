# -*- coding: utf-8 -*-
import os
import json
import copy

import flask
import requests

import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output, State
from analytics_sdk import OAPDash
from analytics_sdk.utilities import (
    save_archive,
    get_archives,
    get_archive,
    generate_pdf
)

from pages import (
    overview,
    client_breakdown,
    resource_breakdown,
    metering_concepts,
)


PLATFORM_ROUTE = os.getenv("PLATFORM_ROUTE", '')
in_store_id = "_oap_data_in_" + PLATFORM_ROUTE
out_store_id = "_oap_data_out_" + PLATFORM_ROUTE
oap_name = os.getenv("PLATFORM_ROUTE", 'metered-usage-insight')

app = OAPDash(
    name=__name__,
    meta_tags=[{"name": "viewport", "content": "width=device-width"}],
    title="OpsRamp Reports",
    route=PLATFORM_ROUTE
)
server = app.server

# Describe the layout/ UI of the app
app.layout = html.Div(
    [
        dcc.Location(id="url", refresh=False), html.Div(id="page-content")
    ]
)

# Update page
@app.callback(Output("page-content", "children"), [Input("url", "pathname")])
def display_page(pathname):
    pathname = pathname.lstrip('/'+app.route)  # IMP

    if pathname == "client-breakdown":
        return client_breakdown.create_layout(app)
    elif pathname == "resource-breakdown":
        return resource_breakdown.create_layout(app)
    elif pathname == "metering-concepts":
        return metering_concepts.create_layout(app)
    elif pathname == "full-view":
        return (
            overview.create_layout(app),
            client_breakdown.create_layout(app, True),
            resource_breakdown.create_layout(app, True),
            metering_concepts.create_layout(app, True),
        )
    else:
        return overview.create_layout(app)


app.validation_layout = html.Div([
    app.layout,
    overview.create_layout(app),
    client_breakdown.create_layout(app, True),
    resource_breakdown.create_layout(app, True),
    metering_concepts.create_layout(app, True),
])


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


layout = dict(
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

graph_data = dict(
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
        Input(in_store_id, "data"),
    ],
)
def pie_graph_total_usage(search_types):
    layout_pie = copy.deepcopy(layout)

    device_types = ['Events-Only', 'Inventory-Only', 'Up-Down', 'Fully-Managed']
    yy = [27.5, 26.4, 32.3, 13.8]

    data = copy.deepcopy(graph_data)
    data['labels'] = device_types
    data['values'] = yy

    figure = dict(data=[data], layout=layout_pie)
    return figure


@app.callback(
    Output("pie-graph-unweighted-usage", "figure"),
    [
        Input(in_store_id, "data"),
    ],
)
def pie_graph_unweighted_usage(search_types):
    layout_pie = copy.deepcopy(layout)

    device_types = ['Client A', 'Client B', 'Client C', 'Client D']
    yy = [27.5, 26.4, 32.3, 13.8]

    data = copy.deepcopy(graph_data)
    data['labels'] = device_types
    data['values'] = yy

    figure = dict(data=[data], layout=layout_pie)
    return figure


@app.callback(
    Output("pie-graph-weighted-usage", "figure"),
    [
        Input(in_store_id, "data"),
    ],
)
def pie_graph_weighted_usage(search_types):
    layout_pie = copy.deepcopy(layout)

    device_types = ['Client A', 'Client B', 'Client C', 'Client D']
    yy = [27.5, 26.4, 32.3, 13.8]

    data = copy.deepcopy(graph_data)
    data['labels'] = device_types
    data['values'] = yy

    figure = dict(data=[data], layout=layout_pie)
    return figure


@app.callback(
    Output("pie-graph-unweighted-type-usage", "figure"),
    [
        Input(in_store_id, "data"),
    ],
)
def pie_graph_unweighted_type_usage(search_types):
    layout_pie = copy.deepcopy(layout)
    layout_pie['legend'] = dict(
        font=dict(color="#333", size="10"),
        orientation="v",
        bgcolor="rgba(0,0,0,0)",
        y=0.1
    )
    layout_pie['margin'] = dict(l=0, r=50, b=00, t=00)

    device_types = ['Type A', 'Type B', 'Type C', 'Type D', 'Type E', 'Type F']
    yy = [27.5, 26.4, 32.3, 13.8, 7, 6]

    data = copy.deepcopy(graph_data)
    data['labels'] = device_types
    data['values'] = yy

    figure = dict(data=[data], layout=layout_pie)
    return figure


@app.callback(
    Output("pie-graph-weighted-type-usage", "figure"),
    [
        Input(in_store_id, "data"),
    ],
)
def pie_graph_weighted_type_usage(search_types):
    layout_pie = copy.deepcopy(layout)
    layout_pie['legend'] = dict(
        font=dict(color="#333", size="10"),
        orientation="v",
        bgcolor="rgba(0,0,0,0)",
        y=0.1
    )

    device_types = ['Type A', 'Type B', 'Type C', 'Type D', 'Type E', 'Type F']
    yy = [27.5, 26.4, 32.3, 13.8, 7, 6]

    data = copy.deepcopy(graph_data)
    data['labels'] = device_types
    data['values'] = yy

    figure = dict(data=[data], layout=layout_pie)
    return figure


# api integration
@app.callback(
    Output('total_clients', 'children'),
    Input('gen-pdf', 'n_clicks'),
    State(out_store_id, 'data')
)
def get_total_clients(n_clicks, data):
    if not n_clicks:  # initial loading
        url = f'https://asura.opsramp.net/api/v2/tenants/msp_21998/clients/search'
        res = requests.get(url, verify=False, cookies=flask.request.cookies)
        total_clients = '-'
        if res.status_code == 200:
            total_clients = res.json()['totalResults']

        return total_clients


@app.callback(
    Output('total_resources', 'children'),
    Input('gen-pdf', 'n_clicks'),
    State(out_store_id, 'data')
)
def get_total_resources(n_clicks, data):
    if not n_clicks:  # initial loading
        url = f'https://asura.opsramp.net/api/v2/tenants/msp_21998/resources/search'
        res = requests.get(url, verify=False, cookies=flask.request.cookies)
        total_resources = '-'
        if res.status_code == 200:
            total_resources = res.json()['totalResults']

        return total_resources


if __name__ == "__main__":
    app.run_server(debug=True)
