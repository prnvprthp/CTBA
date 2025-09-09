import dash 
from dash import html

dash.register_page(__name__, path="/")

layout = html.Div([
    html.H1("Welcome to our Dash App"), 
    
    html.Div("This is where we will write a description", className="block block-top"),
    
    html.Div([
        html.Div("Throw some heavy statistics here", className="block"),
        html.Div("Maybe a graph or heavy statistics here", className="block")
    ], className="row-2"),
    
    html.Div("Brief Overview before we really dive in", className="block block-footer"),  
    
    html.Small("Jackson Shelton, Justin Varela, Pranav Prathap, Yixuan Tan", className="footer-small")
])

