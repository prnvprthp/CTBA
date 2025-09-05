import dash
from dash import html

dash.register_page(__name__, path = '/page1', name = 'Page 1')

layout = html.Div([
    html.H1("This is the 1st Page"),

    #Top Row
    html.Div('Top Row with 1 Column', className='block block-top'),
    
    ## Middle 2 Columns
    html.Div([
        html.Div('Middle Left', className = 'block'),
        html.Div('Middle Right', className='block')
    ], className='row-2'),

    ## Bottom Row / Footer
    html.Div('Footer', className = 'block block-footer')

], className='page1-grid')
