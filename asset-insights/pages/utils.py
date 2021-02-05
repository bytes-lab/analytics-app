from datetime import date

import dash_html_components as html
import dash_core_components as dcc


def Header(app):
    return html.Div([get_header(app), html.Br([])])


def NavBar(app):
    nav_bar = html.Div(
        [
            html.Img(
                src=app.get_asset_url("dash-financial-logo.png"),
                className="logo",
            ),
            html.Div(
                [
                    html.Button(
                        [
                            html.Img(src=app.get_asset_url("pdf-icon.png"), className="action-icon"),
                            html.Span("Save PDF")
                        ],
                        id="gen-pdf",
                        n_clicks=0,
                        className="save-pdf-link btn btn-action d-flex",
                    )
                ],
                className="pull-right mr-3",
            ),
            html.Div(
                [
                    dcc.Dropdown(
                        style={'width': '105px', 'margin-top': '5px'},
                        id="list-archives"
                    ),
                    html.Button(
                        [
                            html.Img(src=app.get_asset_url("archive-icon.png"), className="action-icon"),
                            html.Span("Save")
                        ],
                        n_clicks=0,
                        id="gen-archive",
                        className="save-link btn btn-action d-flex mx-2",
                    ),
                ],
                className="pull-right d-flex",
            ),
        ],
        className="nav-bar d-print-none"
    )

    return nav_bar


def get_header(app):
    route_prefix = '/'+app.route if app.route else ''  # IMP

    header = html.Div(
        [
            html.Div(
                [
                    html.Div(
                        [html.H5("Asset Insights"), html.H6("Februray's Assets")],
                        className="seven columns main-title",
                    )
                ],
                className="twelve columns",
                style={"padding-left": "0", "margin-top": "32px"},
            ),
        ],
        className="row mx-0",
    )
    return header


def get_settings_panel(app):
    settings_panel = html.Div(
        [
            html.H5("App Settings", style={"font-size": "2rem"}),
            html.H6("Reporting Period", className="mt-2 mb-1"),
            dcc.DatePickerRange(
                id='reporting_priod_picker',
                # min_date_allowed=date(1995, 8, 5),
                # max_date_allowed=date(2017, 9, 19),
                # initial_visible_month=date(2020, 9, 5),
            )
        ],
        className="left-panel d-print-none"
    )

    return settings_panel
