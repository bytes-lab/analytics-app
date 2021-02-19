from datetime import date

import dash_html_components as html
import dash_core_components as dcc


def Header(app):
    return html.Div([get_header(app), html.Br([])])


def get_header(app):
    route_prefix = '/'+app.route if app.route else ''  # IMP

    header = html.Div(
        [
            html.Div(
                [
                    html.Div(
                        [
                            html.H5("Hello World App"),
                            html.H6("North America", className="sub-title mt-2")
                        ],
                        className="twelve columns",
                    )
                ],
                className="twelve columns",
                style={"padding-left": "1cm", "margin-top": "32px"},
            ),
        ],
        className="row mx-0",
    )
    return header
