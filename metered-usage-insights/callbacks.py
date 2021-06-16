import os
import time

from dash.dependencies import Input, Output, State

from utils import *
from pages.utils import *


PLATFORM_ROUTE = os.getenv("PLATFORM_ROUTE", '')
in_store_id = "_oap_data_in_" + PLATFORM_ROUTE
out_store_id = "_oap_data_out_" + PLATFORM_ROUTE
oap_name = os.getenv("PLATFORM_ROUTE", 'metered-usage-insight')

def register_callbacks(app):

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
        Input(in_store_id, 'data')
    )
    def pie_graph_total_usage(run_id):
        breakdown_resource_tier = get_breakdown_resource_tier(run_id)

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
        Input(in_store_id, 'data')
    )
    def pie_graph_unweighted_usage(run_id):
        breakdown_client = get_breakdown_client(run_id)
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
        Input(in_store_id, 'data')
    )
    def pie_graph_weighted_usage(run_id):
        breakdown_client = get_breakdown_client(run_id)

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
        Input(in_store_id, 'data')
    )
    def bar_graph_top_10_clients_weighted(run_id):
        breakdown_client = get_breakdown_client(run_id)
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
        Input(in_store_id, 'data')
    )
    def bar_graph_bottom_10_clients_weighted(run_id):
        breakdown_client = get_breakdown_client(run_id)
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
        Input(in_store_id, 'data')
    )
    def pie_graph_unweighted_type_usage(run_id):
        breakdown_resource_type = get_breakdown_resource_type(run_id)
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
        Input(in_store_id, 'data')
    )
    def bar_graph_top_10_resource_type_weighted(run_id):
        breakdown_resource_type = get_breakdown_resource_type(run_id)
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
        Input(in_store_id, 'data')
    )
    def bar_graph_bottom_10_resource_type_weighted(run_id):
        breakdown_resource_type = get_breakdown_resource_type(run_id)
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
        Input(in_store_id, 'data')
    )
    def bar_graph_weighted_time(run_id):
        breakdown_time = get_breakdown_time(run_id)
        _breakdown_time = [(key, val) for key, val in breakdown_time.items()]
        _breakdown_time = sorted(_breakdown_time, key=lambda k: k[0])

        bar_data = {
            'x': [time.strftime('%H:%M', time.localtime(ii[0]))
                  for ii in _breakdown_time[:12]],
            'y': [ii[1] for ii in _breakdown_time[:12]],
            'line': {"color": "#0077c8"},
        }

        figure = {
            "data": [bar_data],
            "layout": bar_graph_layout,
        }

        return figure

    @app.callback(
        Output("pie-graph-weighted-type-usage", "figure"),
        Input(in_store_id, 'data')
    )
    def pie_graph_weighted_type_usage(run_id):
        breakdown_resource_type = get_breakdown_resource_type(run_id)

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
        Input(in_store_id, 'data')
    )
    def table_resource_type(run_id):
        breakdown_resource_tier = get_breakdown_resource_tier(run_id)
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
        Input(in_store_id, 'data')
    )
    def get_total_clients(run_id):
        tenants = get_tenants(run_id)
        return len(tenants)

    @app.callback(
        Output('total_resources', 'children'),
        Input(in_store_id, 'data')
    )
    def get_total_resources(run_id):
        resource_types = get_resource_types(run_id)
        return len(resource_types)
