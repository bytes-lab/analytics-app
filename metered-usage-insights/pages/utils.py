from datetime import date

import dash_html_components as html
import dash_core_components as dcc


def Header(app):
    return html.Div([get_header(app), html.Br([]), get_menu(app)])


def NavBar(app):
    nav_bar = html.Div(
        [
            html.Img(
                src=app.get_asset_url("opsramp-logo.png"),
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
                        [
                            html.H5("Metered Usage Insights"),
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


def get_menu(app):
    route_prefix = '/'+app.route if app.route else ''  # IMP

    menu = html.Div(
        [
            dcc.Link(
                "OVERVIEW",
                href=f"{route_prefix}/overview",
                className="tab first",
            ),
            dcc.Link(
                "CLIENT BREAKDOWN",
                href=f"{route_prefix}/client-breakdown",
                className="tab",
            ),
            dcc.Link(
                "RESOURCE BREAKDOWN",
                href=f"{route_prefix}/resource-breakdown",
                className="tab"
            ),
            dcc.Link(
                "METERING CONCEPTS",
                href=f"{route_prefix}/metering-concepts",
                className="tab",
            ),
        ],
        className="row all-tabs",
        style={ "margin-left": "1cm" }
    )
    return menu


def render_table(table_rows):
    """ Return a dash definition of an HTML table for a list of list """
    table = []

    header = table_rows[0]
    html_row = []
    for item in header:
        html_row.append(html.Td([html.B(item)], className="pl-2"))
    table.append(html.Tr(html_row))

    for row in table_rows[1:-1]:
        html_row = []
        for item in row:
            html_row.append(html.Td([item], className="pl-2"))
        table.append(html.Tr(html_row))

    footer = table_rows[-1]
    html_row = []
    for item in footer:
        html_row.append(html.Td([html.B(item)], className="pl-2"))
    table.append(html.Tr(html_row))

    return table


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
