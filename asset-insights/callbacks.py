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


    # api integration
    # total_managed_resources
    @app.callback(
        Output('total_managed_resources', 'children'),
        Input(in_store_id, 'data')    
    )
    def get_total_managed_resources(run_id):
        managed_resources = get_managed_resources(run_id)
        return managed_resources
    	
    #Managed Resources(bar-graph)
    @app.callback(
        Output("bar-graph-managed-resources", "figure"),
        Input(in_store_id, 'data')
    )
    def bar_graph_managed_resources(run_id):
        breakdown_time = get_managed_resources_breakdown_time(run_id)
        d = {int(k):int(v) for k,v in breakdown_time.items()}
        _breakdown_time = [(key, val) for key, val in d.items()]
        _breakdown_time = sorted(_breakdown_time, key=lambda k: k[0])

        bar_data = {
            'x': [time.strftime('%m/%e', time.localtime(ii[0]))
                  for ii in _breakdown_time[:12]],
            'y': [ii[1] for ii in _breakdown_time[:12]],
            'line': {"color": "#0077c8"},
        }

        figure = {
            "data": [bar_data],
            "layout": bar_graph_layout,
        }

        return figure
    
   	
    # Top Resource types
    @app.callback(
        Output("pie-graph-top-resource-types", "figure"),
        Input(in_store_id, 'data')
    )
    def pie_graph_top_resource_types(run_id):
        breakdown_top_resource_type = get_breakdown_top_resource_type(run_id)
        resource_types = sorted(breakdown_top_resource_type, key=lambda k: -k['count'])

        x_values = [ii['name'].title() for ii in resource_types[:5]] + ['Other']
        y_values = [ii['count'] for ii in resource_types[:5]] + [sum([ii['count'] for ii in resource_types[5:]])]
        data = dict(pie_graph_data)
        data['labels'] = x_values
        data['values'] = y_values

        figure = dict(data=[data], layout=pie_graph_layout)

        return figure

    	
    # Top clients by total managed resources
    @app.callback(
        Output("pie-graph-top-clients-total-managed-resources", "figure"),
        Input(in_store_id, 'data')
    )
    def pie_graph_top_clients_total_managed_resources(run_id):
        breakdown_top_clients_managed_resource = get_breakdown_top_clients_total_managed_resources(run_id)
        resource_types = sorted(breakdown_top_clients_managed_resource, key=lambda k: -k['count'])

        x_values = [ii['clientId'].title() for ii in resource_types[:5]] + ['Other']
        y_values = [ii['count'] for ii in resource_types[:5]] + [sum([ii['count'] for ii in resource_types[5:]])]
        data = dict(pie_graph_data)
        data['labels'] = x_values
        data['values'] = y_values

        figure = dict(data=[data], layout=pie_graph_layout)

        return figure


    #Public cloud vs data center
    @app.callback(
        Output("pie-graph-public-cloud-data-center", "figure"),
        Input(in_store_id, 'data')
    )
    def pie_graph_public_cloud_data_center(run_id):
        public_cloud_data_center = get_breakdown_public_cloud_data_center(run_id)
        resource_types = sorted(public_cloud_data_center, key=lambda k: -k['count'])

        x_values = [ii['name'].title() for ii in resource_types]
        y_values = [ii['count'] for ii in resource_types]
        data = dict(pie_graph_data)
        data['labels'] = x_values
        data['values'] = y_values

        figure = dict(data=[data], layout=pie_graph_layout)

        return figure


        
    #Resource cmposition by public cloud
    @app.callback(
        Output("pie-graph-resource-composition-public-cloud", "figure"),
        Input(in_store_id, 'data')
    )
    def pie_graph_resource_composition_public_cloud(run_id):
        resource_composition = get_breakdown_resource_composition_public_cloud(run_id)
        resource_types = sorted(resource_composition, key=lambda k: -k['count'])

        x_values = [ii['make'].title() for ii in resource_types]
        y_values = [ii['count'] for ii in resource_types]
        data = dict(pie_graph_data)
        data['labels'] = x_values
        data['values'] = y_values

        figure = dict(data=[data], layout=pie_graph_layout)

        return figure

        
    breakdown_pie_graph_layout = dict(
        autosize=True,
        automargin=True,
        height=150,
        margin=dict(l=30, r=300, b=00, t=00),
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

    #Breakdown by operating system (servers)
    @app.callback(
        Output("pie-graph-breakdown-operating-system", "figure"),
        Input(in_store_id, 'data')
    )
    def pie_graph_breakdown_operating_system(run_id):
        breakdown_operating_system = get_breakdown_by_operating_system(run_id)
        resource_types = sorted(breakdown_operating_system, key=lambda k: -k['count'])

        x_values = [ii['osName'].title() for ii in resource_types]
        y_values = [ii['count'] for ii in resource_types]
        data = dict(pie_graph_data)
        data['labels'] = x_values
        data['values'] = y_values

        figure = dict(data=[data], layout=breakdown_pie_graph_layout)

        return figure
    
    '''# Resource composition of web services
    @app.callback(
        Output("pie-graph-resource-composition-web-services", "figure"),
        Input(in_store_id, 'data')
    )
    def pie_graph_resource_composition_web_services(data):
        breakdown_resource_tier = get_breakdown_resource_tier(data, data)

        x_values = []
        y_values = []

        for metric_name, values in breakdown_resource_tier.items():
            x_values.append(metric_name.title())
            y_values.append(values['unweighted']+values['weighted'])

        data = dict(pie_graph_data)
        data['labels'] = x_values
        data['values'] = y_values

        figure = dict(data=[data], layout=pie_graph_layout)

        return figure'''
