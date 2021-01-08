import dash_core_components as dcc
import dash_html_components as html
import plotly.graph_objs as go
from utils import *


def create_layout(app, embedded=False):
    return html.Div([
        NavBar(app) if not embedded else [],
        html.Div(
            [
                Header(app),
                # page 2
                html.Div(
                    [
                        # Row
                        html.Div(
                            [
                                html.Div(
                                    [
                                        html.H6(
                                            ["Unweighted usage by client"], className="subtitle padded"
                                        ),
                                        dcc.Graph(
                                            id="pie-graph-unweighted-usage",
                                            config={"displayModeBar": False},
                                        ),
                                    ],
                                    className="six columns",
                                ),
                                html.Div(
                                    [
                                        html.H6(
                                            ["Weighted usage by client"],
                                            className="subtitle padded",
                                        ),
                                        dcc.Graph(
                                            id="pie-graph-weighted-usage",
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
                                        html.H6("Top 10 clients by weighted usage", className="subtitle padded"),
                                        dcc.Graph(
                                            id="graph-11",
                                            figure={
                                                "data": [
                                                    go.Bar(
                                                        x=[
                                                            "Client A",
                                                            "Client B",
                                                            "Client C",
                                                            "Client D",
                                                            "Client E",
                                                            "Client F",
                                                            "Client G",
                                                            "Client X",
                                                            "Client Y",
                                                            "Client Z",
                                                        ],
                                                        y=[
                                                            "3500.62",
                                                            "2500.67",
                                                            "2100.67",
                                                            "1500.62",
                                                            "1300.26",
                                                            "1200.11",
                                                            "1100.11",
                                                            "1000.26",
                                                            "800.37",
                                                            "700.37",
                                                        ],
                                                        marker={
                                                            "color": "#0077c8",
                                                            "line": {
                                                                "color": "rgb(255, 255, 255)",
                                                                "width": 2,
                                                            },
                                                        },
                                                        name="Calibre Index Fund",
                                                    )
                                                ],
                                                "layout": go.Layout(
                                                    autosize=False,
                                                    bargap=0.65,
                                                    font={"family": "Raleway", "size": 10},
                                                    height=200,
                                                    hovermode="closest",
                                                    legend={
                                                        "x": -0.0228945952895,
                                                        "y": -0.189563896463,
                                                        "orientation": "h",
                                                        "yanchor": "top",
                                                    },
                                                    margin={
                                                        "r": 0,
                                                        "t": 20,
                                                        "b": 20,
                                                        "l": 30,
                                                    },
                                                    showlegend=False,
                                                    title="",
                                                    # width=330,
                                                    xaxis={
                                                        "autorange": True,
                                                        "range": [-0.5, 4.5],
                                                        "showline": True,
                                                        "title": "",
                                                        "type": "category",
                                                    },
                                                    yaxis={
                                                        "autorange": True,
                                                        "range": [0, 3200.9789473684],
                                                        "showgrid": True,
                                                        "showline": True,
                                                        "title": "",
                                                        "type": "linear",
                                                        "zeroline": False,
                                                    },
                                                ),
                                            },
                                            config={"displayModeBar": False},
                                        ),
                                    ],
                                    className="twelve columns",
                                )
                            ],
                            className="row mx-0",
                        ),
                        # Row 3
                        html.Div(
                            [
                                html.Div(
                                    [
                                        html.H6("Bottom 10 clients by weighted usage", className="subtitle padded"),
                                        dcc.Graph(
                                            id="graph-12",
                                            figure={
                                                "data": [
                                                    go.Bar(
                                                        x=[
                                                            "Client A",
                                                            "Client B",
                                                            "Client C",
                                                            "Client D",
                                                            "Client E",
                                                            "Client F",
                                                            "Client G",
                                                            "Client X",
                                                            "Client Y",
                                                            "Client Z",
                                                        ],
                                                        y=[
                                                            "700.37",
                                                            "800.37",
                                                            "1000.26",
                                                            "1100.11",
                                                            "1200.11",
                                                            "1300.26",
                                                            "1500.62",
                                                            "2100.67",
                                                            "2400.67",
                                                            "2500.62",
                                                        ],
                                                        marker={
                                                            "color": "#0077c8",
                                                            "line": {
                                                                "color": "rgb(255, 255, 255)",
                                                                "width": 2,
                                                            },
                                                        },
                                                        name="Calibre Index Fund",
                                                    )
                                                ],
                                                "layout": go.Layout(
                                                    autosize=False,
                                                    bargap=0.65,
                                                    font={"family": "Raleway", "size": 10},
                                                    height=200,
                                                    hovermode="closest",
                                                    legend={
                                                        "x": -0.0228945952895,
                                                        "y": -0.189563896463,
                                                        "orientation": "h",
                                                        "yanchor": "top",
                                                    },
                                                    margin={
                                                        "r": 0,
                                                        "t": 20,
                                                        "b": 20,
                                                        "l": 30,
                                                    },
                                                    showlegend=False,
                                                    title="",
                                                    # width=330,
                                                    xaxis={
                                                        "autorange": True,
                                                        "range": [-0.5, 4.5],
                                                        "showline": True,
                                                        "title": "",
                                                        "type": "category",
                                                    },
                                                    yaxis={
                                                        "autorange": True,
                                                        "range": [0, 3200.9789473684],
                                                        "showgrid": True,
                                                        "showline": True,
                                                        "title": "",
                                                        "type": "linear",
                                                        "zeroline": False,
                                                    },
                                                ),
                                            },
                                            config={"displayModeBar": False},
                                        ),
                                    ],
                                    className="twelve columns",
                                )
                            ],
                            className="row mx-0",
                        )
                    ],
                    className="sub_page",
                ),
            ],
            className="page",
        ),
        get_settings_panel(app)
    ])