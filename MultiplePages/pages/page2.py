import dash
from dash import html

dash.register_page(__name__, path = '/page2', name = 'Page 2')

layout = html.Div([
    html.H3('This is the 2nd Page'),
    html.P('Content on the second page')
])
