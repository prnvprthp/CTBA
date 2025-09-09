import dash
from dash import dcc, html, Input, Output, callback
import plotly.express as px
import pandas as pd
import requests
import datetime

dash.register_page(__name__, path="/page3", name="Page 3")

url = "https://api.stlouisfed.org/fred/series/observations"
fred_api_key = "6f7ac74fe0490f6cd637c636a4c54db5"

series_identifiers = [
    "USMINE", "USCONS", "MANEMP", "DMANEMP", "NDMANEMP",
    "USWTRADE", "USTRADE", "CES4300000001", "CES4422000001",
    "USINFO", "USFIRE", "USPBS", "USEHS", "USLAH", "USSERV", "USGOVT"
]

series_labels = [
    "Mining and Logging", "Construction", "Manufacturing",
    "Durable Goods", "Nondurable Goods", "Wholesale Trade",
    "Retail Trade", "Transportation and Warehousing", "Utilities",
    "Information", "Financial Activities", "Professional and Business Services",
    "Education and Health Services", "Leisure and Hospitality",
    "Other Services", "Government"
]

df = pd.DataFrame(columns=["date", "value", "id"])

for i in range(len(series_identifiers)):
    params = {
        "series_id": series_identifiers[i],
        "api_key": fred_api_key,
        "file_type": "json"
    }
    response = requests.get(url, params=params)
    if response.status_code == 200:
        data = response.json()
        obs = data.get("observations", [])
        dftemp = pd.DataFrame(obs)
        dftemp["id"] = series_labels[i]
        dftemp["value"] = pd.to_numeric(dftemp["value"], errors="coerce")
        dftemp["date"] = pd.to_datetime(dftemp["date"], errors="coerce")
        df = pd.concat([df, dftemp], ignore_index=True)

layout = html.Div([
    html.H3("Industry Employment Statistics"),
    
    html.Div("Select Industries to Chart"),
    dcc.Checklist(
        options=[{"label": industry, "value": industry} for industry in series_labels],
        id="checklist",
        value=["Manufacturing"],
        inline=True
    ),
    
    dcc.Graph(id="checkout-page3"),
    
    dcc.DatePickerRange(
        id="daterange",
        start_date=datetime.datetime(year=1960, month=1, day=1),
        end_date=datetime.date.today()
    ),
    
    html.Br(),
    html.A("Home", href="/", style={"fontSize": "18px"})
])

@callback(
    Output("checkout-page3", "figure"),
    Input("checklist", "value"),
    Input("daterange", "start_date"),
    Input("daterange", "end_date")
)

def update(industries, start, end):
    if not industries:
        return px.line(title="No industries selected")
    
    start = pd.to_datetime(start)
    end = pd.to_datetime(end)

    filtered_df = df[df["id"].isin(industries)]
    filtered_df = filtered_df[(filtered_df["date"] >= start) & (filtered_df["date"] <= end)]

    fig = px.line(filtered_df, x="date", y="value", color="id",
                  labels={"value": "Employment", "date": "Date"})
    fig.update_layout(title="Employment Trends by Industry")
    return fig