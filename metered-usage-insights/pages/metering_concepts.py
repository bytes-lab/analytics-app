import dash_html_components as html

from pages.utils import *


def create_layout(app, embedded=False):
    return html.Div([
        html.Div(
            [
                Header(app),
                # page 6
                html.Div(
                    [
                        # Row 1
                        html.Div(
                            [
                                html.Div(
                                    [
                                        html.H6("Concept definitions", className="subtitle padded"),
                                        html.Br([]),
                                        html.Div(
                                            [
                                                html.P(
                                                    [html.B("Resource Type: "), html.Span("the classification of a resource as defined by OpsRamp.")]
                                                ),
                                                html.P(
                                                    [html.B("Metering Tier: "), html.Span("a classification of a resource based on the level of management Opsramp provides on the resource. There are 4 metering tiers:")]
                                                ),
                                            ],
                                            style={"color": "#7a7a7a"},
                                        ),
                                    ],
                                    className="",
                                ),
                                html.Div(
                                    [
                                        html.Br([]),
                                        html.Div(
                                            [
                                                html.Li([html.B("Inventory-only resource: "), html.Span("a resource that is discovered and tracked by Opsramp as an asset, but is not monitored by Opsramp.")], className="mb-4"),
                                                html.Li([html.B("Events-only resource: "), html.Span("a resource that is monitored by a 3rd party tool, from which Opsramp ingests only events, but not metrics")], className="mb-4"),
                                                html.Li([html.B("Up-down-only resource: "), html.Span("a resource that is monitored by Opsramp only for availability (up/down) status via network ping.")], className="mb-4"),
                                                html.Li([html.B("Fully-managed resource: "), html.Span("a resource from which Opsramp collects multiple metrics for monitoring.")], className="mb-4")
                                            ],
                                            id="reviews-bullet-pts",
                                            className="ml-4"
                                        ),
                                        html.Br([]),
                                        html.Div(
                                            [
                                                html.P(
                                                    [html.B("Weight: "), html.Span("the weight of a resource is a function of the (1) resources's metering tier and (2) for fully-managed resources, the resource's metering class.")]
                                                ),
                                                html.P([html.B("Standard Resource: "), html.Span("the count of a resource type after its weight has been applied to it: this is what Opsramp bills for.")]),
                                                html.P([html.B("Metered Usage: "), html.Span("the hourly standard resource count for a given hour or the average hourly resource over a billing period.")]),
                                                html.Br([]),
                                                html.P(
                                                    ["For more information, click ", html.A("here", href="https://www.google.com", style={"color": "#0077c8"})]
                                                ),
                                            ],
                                            style={"color": "#7a7a7a"},
                                        ),
                                    ],
                                    className="",
                                ),
                            ],
                            className=" ",
                        )
                    ],
                    className="sub_page",
                ),
            ],
            className="page",
        ),
    ])
