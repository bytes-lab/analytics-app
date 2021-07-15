import dash_core_components as dcc
import dash_html_components as html
import plotly.graph_objs as go

from pages.utils import *


def create_layout(app, embedded=False):
    # Page layouts
    return html.Div(
        [
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
                                            html.H6(
                                                ["Summary"], className="subtitle padded"
                                            ),
                                            html.Br(),
                                            html.Div("This application will give users inventory information of their managed devices."),
                                            html.Br(),
                                            html.Div([html.B("Analysis Peirod"), html.Span("9/1/20 8:00 AM PDT - 9/14/20 8:00 AM PDT", style={"margin-left": "50px"})]),
                                            html.Br(),
                                            html.Div([html.B("Client"), html.Span("All Clients", style={"margin-left": "100px"})]),
                                            html.Div(
                                                [
                                                    html.Div(
                                                        [
                                                            html.Div(["-"], id="total_managed_resources", className="font-weight-bold mb-2", style={"font-size": "16px"}),
                                                            html.P("Total Managed Resources",className="mb-0")
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
                                                id="bar-graph-managed-resources",
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
                                                "Top resource types",
                                                className="subtitle padded",
                                            ),
                                            dcc.Graph(
                                                id="pie-graph-top-resource-types",
                                                config={"displayModeBar": False},
                                            ),
                                        ],
                                        className="twelve columns",
                                    )
                                ],
                                className="row mx-0 ",
                            ),
                            # Row 6
                            html.Div(
                                [
                                    html.Div(
                                        [
                                            html.H6(
                                                "Top clients by total managed resources",
                                                className="subtitle padded",
                                            ),
                                            dcc.Graph(
                                                id="pie-graph-top-clients-total-managed-resources",
                                                config={"displayModeBar": False},
                                            ),
                                        ],
                                        className="twelve columns",
                                    )
                                ],
                                className="row mx-0 ",
                            ),
                            # Row 7
                            html.Div(
                                [
                                    html.Div(
                                        [
                                            html.H6(
                                                ["Public cloud vs data center"], className="subtitle padded"
                                            ),
                                            dcc.Graph(
                                                id="pie-graph-public-cloud-data-center",
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
                                                id="pie-graph-resource-composition-public-cloud",
                                                config={"displayModeBar": False},
                                            ),
                                        ],
                                        className="six columns",
                                    ),
                                ],
                                className="row mx-0",
                                style={"margin-bottom": "35px"},
                            ),

                            # Row 8
                            html.Div(
                                [
                                   html.Div(
                                        [
                                            html.H6(
                                                ["Breakdown by operating system (servers)"], className="subtitle padded"
                                            ),
                                            dcc.Graph(
                                                id="pie-graph-breakdown-operating-system",
                                                config={"displayModeBar": False},
                                            ),
                                        ],
                                        className="twelve columns",
                                    ),
                                ],
                                className="row mx-0 ",
                            ),

                            # Row 9
                            #html.Div(
                            #    [
                            #        html.Div(
                            #            [
                            #                html.H6(
                            #                    "Resource composition of web services",
                            #                    className="subtitle padded",
                            #                ),
                            #                dcc.Graph(
                            #                    id="pie-graph-resource-composition-web-services",
                            #                    config={"displayModeBar": False},
                            #                ),
                            #           ],
                            #            className="twelve columns",
                            #        ),
                            #    ],
                            #    className="row mx-0",
                            #),
                        ],
                        className="sub_page",
                    ),
                ],
                className="page",
            ),
        ]
    )
