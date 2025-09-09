from dash import html, dcc, Input, Output, register_page, callback
import dash_bootstrap_components as dbc
import pandas as pd
import plotly.express as px

register_page(__name__, path="/FinalPage2", name='Page 2')

# Industry identifiers
series_identifiers = {
    'Mining and Logging': 'NRMN', 'Construction': 'CONS', 'Manufacturing': 'MFG',
    'Trade Transportation & Utilities': 'TRAD', 'Information': 'INFO',
    'Financial Activities': 'FIRE', 'Professional and Business Services': 'PBSV',
    'Education and Health Services': 'EDUH', 'Leisure and Hospitality': 'LEIH',
    'Other Services': 'SRVO', 'Government': 'GOVT'
}

# State code to name mapping
state_code_to_name = {
    'AL': 'Alabama', 'AK': 'Alaska', 'AZ': 'Arizona', 'AR': 'Arkansas','CA': 'California', 'CO': 'Colorado', 'CT': 'Connecticut', 'DE': 'Delaware',
    'DC': 'District of Columbia', 'FL': 'Florida', 'GA': 'Georgia', 'HI': 'Hawaii','ID': 'Idaho', 'IL': 'Illinois', 'IN': 'Indiana', 'IA': 'Iowa',
    'KS': 'Kansas', 'KY': 'Kentucky', 'LA': 'Louisiana', 'ME': 'Maine','MD': 'Maryland', 'MA': 'Massachusetts', 'MI': 'Michigan', 'MN': 'Minnesota',
    'MS': 'Mississippi', 'MO': 'Missouri', 'MT': 'Montana', 'NE': 'Nebraska','NV': 'Nevada', 'NH': 'New Hampshire', 'NJ': 'New Jersey', 'NM': 'New Mexico',
    'NY': 'New York', 'NC': 'North Carolina', 'ND': 'North Dakota', 'OH': 'Ohio','OK': 'Oklahoma', 'OR': 'Oregon', 'PA': 'Pennsylvania', 'RI': 'Rhode Island',
    'SC': 'South Carolina', 'SD': 'South Dakota', 'TN': 'Tennessee', 'TX': 'Texas','UT': 'Utah', 'VT': 'Vermont', 'VA': 'Virginia', 'WA': 'Washington',
    'WV': 'West Virginia', 'WI': 'Wisconsin', 'WY': 'Wyoming'
}

# Load and process data
def fetch_data(industry_key):
    df = pd.read_csv("FinalDF.csv")
    df = df.dropna(subset=['date', 'value_empindustry', 'value_nonfarmemp', 'id', 'state'])

    df['date'] = pd.to_datetime(df['date'], errors='coerce')
    df['value_empindustry'] = pd.to_numeric(df['value_empindustry'], errors='coerce')
    df['value_nonfarmemp'] = pd.to_numeric(df['value_nonfarmemp'], errors='coerce')
    df['value'] = df['value_empindustry'] / df['value_nonfarmemp'] * 100

    df = df[df['id'] == series_identifiers[industry_key]]
    df['state_code'] = df['state']
    df['state'] = df['state_code'].map(state_code_to_name)

    return df.dropna(subset=['value', 'state_code', 'date'])

# Default date
try:
    last_date = fetch_data("Construction")['date'].max()
except Exception:
    last_date = pd.Timestamp("2000-01-01")

# Layout
layout = dbc.Container([
    dbc.Row([
        dbc.Col(
            dbc.Card(
                dbc.CardBody([
                    html.H2("US Employment by Industry", className="card-title"),
                    html.P("Percentage of employees in each industry relative to the non-farm workforce."),
                    html.H5("Select an Industry and Time Period"),

                    html.Div([
                        html.Div([
                            html.Label("Industry"),
                            dcc.Dropdown(
                                id="industry_page2",
                                options=[{"label": k, "value": k} for k in series_identifiers],
                                value="Construction",
                                clearable=False,
                                style={"width": "200px"}
                            )
                        ], style={"marginRight": "20px"}),

                        html.Div([
                            html.Label("Year"),
                            dcc.Dropdown(id="year_page2", clearable=False, style={"width": "120px"})
                        ], style={"marginRight": "20px"}),

                        html.Div([
                            html.Label("Month"),
                            html.Div(
                                dcc.Slider(
                                    id="month_page2",
                                    min=1,
                                    max=12,
                                    step=1,
                                    marks={i: m for i, m in enumerate(
                                        ["Jan", "Feb", "Mar", "Apr", "May", "Jun",
                                         "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"], 1)},
                                    value=last_date.month,
                                    tooltip={"placement": "bottom", "always_visible": True}
                                ),
                                style={"width": "750px", "marginLeft": "auto"}
                            )
                        ])
                    ], style={"display": "flex", "alignItems": "center", "marginBottom": "20px"}),

                    dcc.Graph(id="choropleth_page2"),
                    #html.H5("Top & Bottom 5 States by Employment %", className="mt-4"),
                    dcc.Graph(id="bar_chart_page2")
                ])
            ),
            width=12
        )
    ])
], fluid=True)

# Callback
@callback(
    Output("year_page2", "options"),
    Output("year_page2", "value"),
    Output("choropleth_page2", "figure"),
    Output("bar_chart_page2", "figure"),
    Input("industry_page2", "value"),
    Input("year_page2", "value"),
    Input("month_page2", "value")
)
def update_dropdown_and_map(industry, selected_year, selected_month):
    df = fetch_data(industry)
    if df.empty:
        empty_fig = px.choropleth(title="No Data Available")
        return [], None, empty_fig, px.bar(title="No Data Available")

    years = sorted(df['date'].dt.year.unique())
    year_options = [{"label": str(y), "value": y} for y in years]

    if selected_year is None:
        selected_year = years[-1]
    if selected_month is None:
        selected_month = df['date'].dt.month.max()

    filtered_df = df[
        (df['date'].dt.year == selected_year) &
        (df['date'].dt.month == selected_month)
    ]

    if filtered_df.empty:
        empty_fig = px.choropleth(title="No Data Available for Selected Date")
        return year_options, selected_year, empty_fig, px.bar(title="No Data Available")

    # Choropleth
    map_fig = px.choropleth(
        filtered_df,
        locations="state_code",
        locationmode="USA-states",
        scope="usa",
        color="value",
        hover_name="state",
        color_continuous_scale="Viridis",
        title=f"{industry} Employment - {pd.Timestamp(selected_year, selected_month, 1).strftime('%B %Y')}"
    )

    # Bar chart for top and bottom 5
    top_bottom = pd.concat([
        filtered_df.nlargest(5, 'value'),
        filtered_df.nsmallest(5, 'value')
    ])

    bar_fig = px.bar(
        top_bottom.sort_values('value'),
        x='value',
        y='state',
        orientation='h',
        color='value',
        title=f"Top and Bottom 5 States by Employment % for {industry} - {selected_year}",
        color_continuous_scale='viridis',
        labels={"value": "Employment %", "state": "State"}
    )
    bar_fig.update_layout(yaxis={'categoryorder': 'total ascending'})

    return year_options, selected_year, map_fig, bar_fig
