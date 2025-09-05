import dash
from dash import html

dash.register_page(__name__, path = '/')

layout = html.Div([
    html.H2("Welcome to the home page"),
    html.P("This is a simple multi-page Dash project")
])
