import dash
from dash import html

dash.register_page(__name__, path="/", name="Home")

layout = html.Div([
    html.H1("Analyzing Economic and Employment Trends by Industry and US states")
    ], className='page1-introduction')
