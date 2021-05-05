import dash_core_components as dcc
import dash_html_components as html
import plotly.graph_objs as go

from pages.utils import *


def create_layout(app, embedded=False):
    return html.Div([
        html.Div(
            [
                Header(app),
                # page 4
                html.Div(
                    [
                        # Row 1
                        html.Div(
                            [
                                html.Div(
                                    [
                                        html.H6(
                                            ["Unweighted usage by resource type"], className="subtitle padded"
                                        ),
                                        dcc.Graph(
                                            id="pie-graph-unweighted-type-usage",
                                            config={"displayModeBar": False},
                                        ),
                                    ],
                                    className="six columns",
                                ),
                                html.Div(
                                    [
                                        html.H6(
                                            ["Weighted usage by resource type"],
                                            className="subtitle padded",
                                        ),
                                        dcc.Graph(
                                            id="pie-graph-weighted-type-usage",
                                            config={"displayModeBar": False},
                                        ),
                                    ],
                                    className="six columns",
                                ),
                            ],
                            className="row mx-0",
                        ),
                        # Row 2
                        html.Div(
                            [
                                html.Div(
                                    [
                                        html.H6("Top 10 resource types by weighted usage", className="subtitle padded"),
                                        dcc.Graph(
                                            id="bar-graph-top-10-resource-type-weighted",
                                            config={"displayModeBar": False},
                                        ),
                                    ],
                                    className="twelve columns",
                                )
                            ],
                            className="row mx-0 my-5",
                        ),
                        # Row 3
                        html.Div(
                            [
                                html.Div(
                                    [
                                        html.H6("Bottom 10 resource types by weighted usage", className="subtitle padded"),
                                        dcc.Graph(
                                            id="bar-graph-bottom-10-resource-type-weighted",
                                            config={"displayModeBar": False},
                                        ),
                                    ],
                                    className="twelve columns",
                                )
                            ],
                            className="row mx-0 mt-3",
                        )
                    ],
                    className="sub_page",
                ),
            ],
            className="page",
        ),
    ])