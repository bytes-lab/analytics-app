from datetime import date

import dash_html_components as html
import dash_core_components as dcc


def Header(app):
    return html.Div([get_header(app), html.Br([]), get_menu(app)])


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
                        [html.H5("Metered Usage Insights"), html.H6("North America")],
                        className="seven columns main-title",
                    ),
                    html.Div(
                        [
                            dcc.Link(
                                "Full View",
                                href=f"{route_prefix}/full-view",
                                className="full-view-link",
                            )
                        ],
                        className="five columns d-print-none",
                    ),
                ],
                className="twelve columns",
                style={"padding-left": "0", "margin-top": "32px"},
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
                "Overview",
                href=f"{route_prefix}/overview",
                className="tab first",
            ),
            dcc.Link(
                "Client Breakdown",
                href=f"{route_prefix}/client-breakdown",
                className="tab",
            ),
            dcc.Link(
                "Resource Breakdown",
                href=f"{route_prefix}/resource-breakdown",
                className="tab"
            ),
            dcc.Link(
                "Metering Concepts",
                href=f"{route_prefix}/metering-concepts",
                className="tab",
            ),
        ],
        className="row ml-4 pl-3 all-tabs",
    )
    return menu


def make_dash_table(df):
    """ Return a dash definition of an HTML table for a Pandas dataframe """
    table = []
    for index, row in df.iterrows():
        html_row = []
        for i in range(len(row)):
            html_row.append(html.Td([row[i]]))
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
