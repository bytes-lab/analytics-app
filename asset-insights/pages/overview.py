import dash_core_components as dcc
import dash_html_components as html
import plotly.graph_objs as go

from pages.utils import *


def create_layout(app, embedded=False):
    # Page layouts
    return html.Div(
        [
            NavBar(app) if not embedded else [],
            html.Div(
                [
                    html.Div([Header(app)]),
                    # page 1
                    html.Div(
                        [
                            # Row 3
                            html.Div(
                                [
                                    html.Div(
                                        [
                                            html.H6("Summary", className="subtitle padded"),
                                            html.Br(),
                                            html.Div("This application will give users inventory information of their managed devices."),
                                            html.Br(),
                                            html.Div([html.B("Reporting Peirod"), html.Span("10/1/20 8:00 AM PDT - 10/14/20 8:00 AM PDT", style={"margin-left": "50px"})]),
                                            html.Div([html.B("Client"), html.Span("All clients", style={"margin-left": "110px"})], className="mt-1"),
                                            html.Div(
                                                [
                                                    html.Div(
                                                        [
                                                            html.Div(["-"], id="total_clients", className="font-weight-bold mb-2", style={"font-size": "16px"}),
                                                            html.P("Total managed resources", className="mb-0")
                                                        ],
                                                        className="border border-1 col-12 text-center py-3",
                                                    ),
                                                ],
                                                id="info-container",
                                                className="row mt-4 ml-1",
                                            ),

                                        ],
                                        className="twelve columns",
                                    ),
                                ],
                                className="row mx-0",
                                style={"margin-bottom": "35px"},
                            ),
                            # Row 4
                            html.Div(
                                [
                                    html.Div(
                                        [
                                            html.H6(
                                                "Managed resources",
                                                className="subtitle padded",
                                            ),
                                            dcc.Graph(
                                                id="graph-2",
                                                figure={
                                                    "data": [
                                                        go.Scatter(
                                                            x=[
                                                                "2008",
                                                                "2009",
                                                                "2010",
                                                                "2011",
                                                                "2012",
                                                                "2013",
                                                                "2014",
                                                                "2015",
                                                                "2016",
                                                                "2017",
                                                                "2018",
                                                            ],
                                                            y=[
                                                                "10000",
                                                                "7500",
                                                                "9000",
                                                                "14500",
                                                                "10500",
                                                                "11000",
                                                                "14000",
                                                                "18000",
                                                                "19000",
                                                                "17500",
                                                                "24000",
                                                            ],
                                                            line={"color": "#0077c8"},
                                                            mode="lines+markers",
                                                            name="Usage",
                                                        )
                                                    ],
                                                    "layout": go.Layout(
                                                        autosize=True,
                                                        title="",
                                                        font={"family": "Raleway", "size": 10},
                                                        height=200,
                                                        # width=340,
                                                        hovermode="closest",
                                                        legend={
                                                            "x": 0.45,
                                                            "y": -0.102606516291,
                                                            "orientation": "h",
                                                        },
                                                        margin={
                                                            "r": 20,
                                                            "t": 20,
                                                            "b": 20,
                                                            "l": 50,
                                                        },
                                                        showlegend=True,
                                                        xaxis={
                                                            "autorange": True,
                                                            "nticks": 11,
                                                            "linecolor": "rgb(0, 0, 0)",
                                                            "linewidth": 1,
                                                            "range": [2008, 2018],
                                                            "showgrid": False,
                                                            "showline": True,
                                                            "title": "",
                                                            "type": "linear",
                                                        },
                                                        yaxis={
                                                            "autorange": False,
                                                            "gridcolor": "rgba(127, 127, 127, 0.2)",
                                                            "mirror": False,
                                                            "nticks": 4,
                                                            "range": [0, 30000],
                                                            "showgrid": True,
                                                            "showline": True,
                                                            "ticklen": 1,
                                                            "ticks": "outside",
                                                            "title": "",
                                                            "type": "linear",
                                                            "zeroline": False,
                                                            "zerolinewidth": 4,
                                                        },
                                                    ),
                                                },
                                                config={"displayModeBar": False},
                                            ),
                                        ],
                                        className="twelve columns",
                                    )
                                ],
                                className="row mx-0 ",
                            ),
                            # Row 5
                            html.Div(
                                [
                                    html.Div(
                                        [
                                            html.H6(
                                                "Top 10 resource types",
                                                className="subtitle padded",
                                            ),
                                            dcc.Graph(
                                                id="pie-graph-top-10-resource-types",
                                                config={"displayModeBar": False},
                                            ),
                                        ],
                                        className="twelve columns",
                                    ),
                                ],
                                className="row mx-0",
                                style={"margin-bottom": "35px"},
                            ),
                            html.Div(
                                [
                                    html.Div(
                                        [
                                            html.H6(
                                                "Top clients by total managed resources",
                                                className="subtitle padded",
                                            ),
                                            dcc.Graph(
                                                id="pie-graph-top-clients-by-managed-resources",
                                                config={"displayModeBar": False},
                                            ),
                                        ],
                                        className="twelve columns",
                                    ),
                                ],
                                className="row mx-0",
                                style={"margin-bottom": "35px"},
                            ),
                            html.Div(
                                [
                                    html.Div(
                                        [
                                            html.H6(
                                                "Public cloud vs data center",
                                                className="subtitle padded",
                                            ),
                                            dcc.Graph(
                                                id="pie-graph-public-vs-data",
                                                config={"displayModeBar": False},
                                            ),
                                        ],
                                        className="six columns",
                                    ),
                                    html.Div(
                                        [
                                            html.H6(
                                                "Resource composition by public cloud",
                                                className="subtitle padded",
                                            ),
                                            dcc.Graph(
                                                id="pie-graph-resource-composition-public",
                                                config={"displayModeBar": False},
                                            ),
                                        ],
                                        className="six columns",
                                    ),
                                ],
                                className="row mx-0",
                                style={"margin-bottom": "35px"},
                            ),
                            html.Div(
                                [
                                    html.Div(
                                        [
                                            html.H6(
                                                "Breakdown by operating system (servers)",
                                                className="subtitle padded",
                                            ),
                                            dcc.Graph(
                                                id="pie-graph-breakdown-by-os",
                                                config={"displayModeBar": False},
                                            ),
                                        ],
                                        className="six columns",
                                    ),
                                    html.Div(
                                        [
                                            html.H6(
                                                "Resource composition of web services",
                                                className="subtitle padded",
                                            ),
                                            dcc.Graph(
                                                id="pie-graph-resource-composition-web",
                                                config={"displayModeBar": False},
                                            ),
                                        ],
                                        className="six columns",
                                    ),
                                ],
                                className="row mx-0",
                                style={"margin-bottom": "35px"},
                            ),
                        ],
                        className="sub_page",
                    ),
                ],
                className="page",
            ),
            get_settings_panel(app)
        ]
    )