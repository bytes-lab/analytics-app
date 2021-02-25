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
                                                ["Hello World"], className="subtitle padded"
                                            ),
                                            html.Br(),
                                            html.Div("This app demonstrates how to write your first analytics app."),
                                            html.Br(),
                                            html.Div([html.B("Reporting Period"), html.Span("02/25/21 8:00 AM PST - 02/25/21 1:00 AM PST", style={"margin-left": "50px"})]),
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
                                                            html.P("Resources", className="mb-0")
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
                        ],
                        className="sub_page",
                    ),
                ],
                className="page",
            ),
        ]
    )
