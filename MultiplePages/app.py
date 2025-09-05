from dash import Dash, html, page_container
import dash_bootstrap_components as dbc

## Initialize the app
app = Dash(__name__, use_pages = True, suppress_callback_exceptions=True,title = "Multi Page App")
server = app.server ##for deployment

app.layout = html.Div([
    dbc.NavbarSimple(
        children = [
            dbc.NavLink("Home", href = '/', active = 'exact'),
            dbc.NavLink("Page One", href = '/page1', active = 'exact'),
            dbc.NavLink("Page Two", href = '/page2', active = 'exact')   
         ], 
         brand = 'Multi-Page App'
    ),
    page_container

])

if __name__ == "__main__":
    app.run(debug=True)