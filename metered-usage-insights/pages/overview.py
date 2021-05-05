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
                                            html.Div("This application shows you your OpsRamp usage over the metering period."),
                                            html.Br(),
                                            html.Div([html.B("Reporting Peirod"), html.Span("10/1/20 8:00 AM PDT - 10/14/20 8:00 AM PDT", style={"margin-left": "50px"})]),
                                            html.Div(
                                                [
                                                    html.Div(
                                                        [
                                                            html.Div(["-"], id="total_clients", className="font-weight-bold mb-2", style={"font-size": "16px"}),
                                                            html.P("Clients", className="mb-0")
                                                        ],
                                                        className="border border-1 col-6 text-center py-3",
                                                    ),
                                                    html.Div(
                                                        [
                                                            html.Div(["-"], id="total_resources", className="font-weight-bold mb-2", style={"font-size": "16px"}),
                                                            html.P("Resource Types", className="mb-0")
                                                        ],
                                                        className="border border-1 col-6 text-center py-3",
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
                                                ["Usage Breakdown by resource tier"], className="subtitle padded"
                                            ),
                                            html.Table(id="table-resource-type"),
                                        ],
                                        className="six columns",
                                    ),
                                    html.Div(
                                        [
                                            html.H6(
                                                "Total usage by resource tier",
                                                className="subtitle padded",
                                            ),
                                            dcc.Graph(
                                                id="pie-graph-total-usage",
                                                config={"displayModeBar": False},
                                            ),
                                        ],
                                        className="six columns",
                                    ),
                                ],
                                className="row mx-0",
                                style={"margin-bottom": "35px"},
                            ),
                            # Row 5
                            html.Div(
                                [
                                    html.Div(
                                        [
                                            html.H6(
                                                "Weighted usage",
                                                className="subtitle padded",
                                            ),
                                            dcc.Graph(
                                                id="bar-graph-weighted-time",
                                                config={"displayModeBar": False},
                                            ),
                                        ],
                                        className="twelve columns",
                                    )
                                ],
                                className="row mx-0 ",
                            ),
                        ],
                        className="sub_page",
                    ),
                ],
                className="page",
            ),
        ]
    )
