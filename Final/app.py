from dash import Dash, html, page_container
import dash_bootstrap_components as dbc

app = Dash(__name__,use_pages=True, external_stylesheets=[dbc.themes.FLATLY],suppress_callback_exceptions=True,title="Final Project")
server = app.server

app.layout = html.Div([
    dbc.NavbarSimple(
        children=[
            dbc.NavLink("Home", href="/", active="exact"),
            dbc.NavLink("Page One", href="/FinalPage1", active="exact"),
            dbc.NavLink("Page 2", href="/FinalPage2", active="exact"),
            dbc.NavLink("Page 3", href="/FinalPage3", active="exact")
        ],
        brand="Employment Dashboard",
        color="primary",
        dark=True,
        className="mb-4"
    ),
    page_container
],className='Divstyle')

if __name__ == "__main__":
    app.run(debug=True)
