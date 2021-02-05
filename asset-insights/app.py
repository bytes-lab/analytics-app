# -*- coding: utf-8 -*-
import os

from analytics_sdk import OAPDash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output

from callbacks import register_callbacks
from pages import overview

PLATFORM_ROUTE = os.getenv("PLATFORM_ROUTE", '')

app = OAPDash(
    name=__name__,
    meta_tags=[{"name": "viewport", "content": "width=device-width"}],
    title="OpsRamp Reports",
    route=PLATFORM_ROUTE
)
server = app.server

# Describe the layout/ UI of the app
app.layout = overview.create_layout(app)

register_callbacks(app)

if __name__ == "__main__":
    app.run_server(debug=True)
