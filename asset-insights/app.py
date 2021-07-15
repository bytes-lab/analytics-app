# -*- coding: utf-8 -*-
import os

from analytics_sdk import OAPDash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output

from callbacks import register_callbacks
from engine import compute
from pages import (
    assetsummary,
)

PLATFORM_ROUTE = os.getenv("PLATFORM_ROUTE", '')

app = OAPDash(
    name=__name__,
    meta_tags=[{"name": "viewport", "content": "width=device-width"}],
    title="OpsRamp Reports",
    route=PLATFORM_ROUTE
)
server = app.server
app.server.secret_key = 'super secret key'
# register the compute engine
app._add_url("compute", compute, ['POST'])

# Describe the layout/ UI of the app
app.layout = html.Div(
    [
        dcc.Location(id="url", refresh=False), html.Div(id="page-content")
    ]
)

register_callbacks(app)

app.validation_layout = html.Div([
    app.layout,
    assetsummary.create_layout(app, True),
])

# routing
@app.callback(Output("page-content", "children"), [Input("url", "pathname")])
def display_page(pathname):
    route_prefix = '/'+app.route if app.route else ''
    pathname = pathname.replace(route_prefix+'/', '')  # IMP

    return assetsummary.create_layout(app)


if __name__ == "__main__":
    app.run_server(debug=True)
