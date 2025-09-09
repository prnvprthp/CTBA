import dash
from dash import Dash, Input, Output, html, dcc, callback
import dash_bootstrap_components as dbc
import plotly.express as px
import pandas as pd
import numpy as np
import json
from datetime import datetime
import requests
import datetime
from plotly.subplots import make_subplots
import plotly.graph_objects as go

dash.register_page(__name__, path="/FinalPage3", name="Page 3")

url = 'https://api.stlouisfed.org/fred/series/observations'
fred_api_key = '1d90de899e9698a2924f22d85c093fe6'
series_identifiers = ['CES1000000008', 'CES2000000008', 'CES3000000008', 'CES4000000008','CES5000000008', 'CES5500000008', 'CES6000000008', 'CES6500000008', 'CES7000000008', 'CES8000000008']
series_labels = ['Mining and Logging', 'Construction', 'Manufacturing', 'Trade Transportation and Utilities', 'Information', 'Financial Activities', 'Professional and Business Services', 'Education and Health Services', 'Leisure and Hospitality', 'Other Services']

df = pd.DataFrame(columns = ['realtime_start', 'realtime_end', 'date', 'value', 'id'])

for i in range(len(series_identifiers)):
    
    params = {
    'series_id': series_identifiers[i],
    'api_key': fred_api_key,
    'file_type':'json'
    }
    
    response = requests.get(url, params = params)
    if response.status_code == 200:
        data = response.json()
        obs = data.get('observations', [])
        dftemp = pd.DataFrame(obs)
        dftemp['id'] = series_labels[i]
        dftemp['value'] = pd.to_numeric(dftemp['value'], errors = 'coerce')
        dftemp['date'] = pd.to_datetime(dftemp['date'], errors = 'coerce')
        frame = [df, dftemp]
        df = pd.concat(frame)

params = {
    'series_id': 'CPIAUCSL',
    'api_key':fred_api_key,
    'file_type': 'json'
}
response = requests.get(url, params = params)
if response.status_code == 200:
    data = response.json()
    obs = data.get('observations', [])
    dfrecess = pd.DataFrame(obs)
    dfrecess['value'] = pd.to_numeric(dfrecess['value'], errors = 'coerce')
    dfrecess['date'] = pd.to_datetime(dfrecess['date'], errors = 'coerce')

#controls
controls = html.Div([
    dcc.Checklist(
        options = [
            {'label': industry, 'value': industry} for industry in series_labels
        ],
        id = 'checklist',
        value = []
    )
])

Test_output = dcc.Graph(id = 'checkout')

CPI_Toggle = dcc.Checklist(
    options = [{'label': 'CPI', 'value': 'recess'}],
    id = 'toggle',
    value = []
)

date_control = dcc.DatePickerRange(id = 'daterange',
                                   start_date = datetime.datetime(year = 1968, month = 1, day = 1),
                                   end_date = datetime.date.today(),
                                   min_date_allowed = min(df['date']),
                                   max_date_allowed = datetime.date.today())
                                   
layout = html.Div(
    [
        html.H3("Industry Average Hourly Wage Statistics", className="page-title"),
        
        html.Div(
            [
                html.Div(
                    [
                        html.Div("Select Industries to Chart"),
                        controls,
                    ],
                    className="left-panel"
                ),
                
                html.Div(
                    [
                        dcc.Graph(id="checkout-page3", className="chart-area"),
                        html.Div(
                            [date_control, CPI_Toggle],
                            className="controls-row"
                        ),
                    ],
                    className="right-panel"
                ),
            ],
            className="main-row"
        ),
    
        html.Br(),
        html.A("Home", href="/", className="home-link"),
    ], 
    className="page3-grid"
)

@callback(
    Output('checkout-page3', 'figure'),
    
    
    Input('checklist', 'value'),
    Input('daterange', 'start_date'),
    Input('daterange','end_date'),
    Input('toggle', 'value')
)
def update3(industries, start, end, toggle):
    filtered_df = df[df['id'].isin(industries)]
    filtered_df = filtered_df[filtered_df['date']<= end]
    filtered_df = filtered_df[filtered_df['date']>= start]
    filtered_dfrecess = dfrecess[dfrecess['date']<= end]
    filtered_dfrecess = filtered_dfrecess[dfrecess['date']>= start]
    
    
    if 'recess' in toggle:
        ids = filtered_df['id'].unique()
        fig = make_subplots(specs = [[{'secondary_y': True}]])
        for i in ids:
            df_temp = filtered_df[filtered_df['id']== i ]
            fig.add_trace(
            go.Scatter(x = df_temp['date'], y = df_temp['value'], name = i, mode = 'lines'),
            secondary_y= False,
            )
        fig.add_trace(
        go.Scatter(x = filtered_dfrecess['date'], y = filtered_dfrecess['value'], name = 'Consumer Price Index', mode = 'lines'),
        secondary_y= True,
        )
        
        fig.update_layout(xaxis_title = 'Year', yaxis_title = 'Average Hourly Wage')
        fig.update_yaxes(title_text = 'CPI', secondary_y = True)
        fig.update_yaxes(range = [0, None], secondary_y= False)
    else:
        fig = px.line(filtered_df, x = 'date', y= 'value', color = 'id',
                        labels = {
                            'value': 'Average Hourly Wage',
                            'date':'Year',
                            'id': 'Industry'
                        })
        fig.update_yaxes(range = [0, None])
    
    return fig
