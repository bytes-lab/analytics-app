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
                            html.H5("Asset Insights"),
                            html.H6("September's Assets", className="sub-title mt-2")
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
