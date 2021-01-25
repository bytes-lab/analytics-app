# -*- coding: utf-8 -*-
import os

from analytics_sdk import OAPDash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output

from callbacks import register_callbacks
from pages import (
    overview,
    client_breakdown,
    resource_breakdown,
    metering_concepts,
)

PLATFORM_ROUTE = os.getenv("PLATFORM_ROUTE", '')

app = OAPDash(
    name=__name__,
    meta_tags=[{"name": "viewport", "content": "width=device-width"}],
    title="OpsRamp Reports",
    route=PLATFORM_ROUTE
)

# Describe the layout/ UI of the app
app.layout = html.Div(
    [
        dcc.Location(id="url", refresh=False), html.Div(id="page-content")
    ]
)

register_callbacks(app)

app.validation_layout = html.Div([
    app.layout,
    overview.create_layout(app),
    client_breakdown.create_layout(app, True),
    resource_breakdown.create_layout(app, True),
    metering_concepts.create_layout(app, True),
])

# routing
@app.callback(Output("page-content", "children"), [Input("url", "pathname")])
def display_page(pathname):
    route_prefix = '/'+app.route if app.route else ''
    pathname = pathname.replace(route_prefix+'/', '')  # IMP

    if pathname == "client-breakdown":
        return client_breakdown.create_layout(app)
    elif pathname == "resource-breakdown":
        return resource_breakdown.create_layout(app)
    elif pathname == "metering-concepts":
        return metering_concepts.create_layout(app)
    elif pathname == "full-view":
        return (
            overview.create_layout(app),
            client_breakdown.create_layout(app, True),
            resource_breakdown.create_layout(app, True),
            metering_concepts.create_layout(app, True),
        )
    else:
        return overview.create_layout(app)


if __name__ == "__main__":
    app.run_server(debug=True)
