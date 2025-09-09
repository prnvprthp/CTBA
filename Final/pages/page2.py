from dash import html, dcc, Input, Output, register_page, callback
import pandas as pd
import plotly.express as px

register_page(__name__, path="/page2", name='Page TWO')

series_identifiers = {
    'Mining and Logging': 'NRMN', 'Construction': 'CONS', 'Manufacturing': 'MFG',
    'Trade Transportation & Utilities': 'TRAD', 'Information': 'INFO',
    'Financial Activities': 'FIRE', 'Professional and Business Services': 'PBSV',
    'Education and Health Services': 'EDUH', 'Leisure and Hospitality': 'LEIH',
    'Other Services': 'SRVO', 'Government': 'GOVT'
}

state_code_to_name = {
    'AL': 'Alabama', 'AK': 'Alaska', 'AZ': 'Arizona', 'AR': 'Arkansas','CA': 'California', 'CO': 'Colorado', 'CT': 'Connecticut', 'DE': 'Delaware','DC': 'District of Columbia', 'FL': 'Florida', 'GA': 'Georgia', 'HI': 'Hawaii','ID': 'Idaho', 'IL': 'Illinois', 'IN': 'Indiana', 'IA': 'Iowa','KS': 'Kansas', 'KY': 'Kentucky', 'LA': 'Louisiana', 'ME': 'Maine','MD': 'Maryland', 'MA': 'Massachusetts', 'MI': 'Michigan', 'MN': 'Minnesota','MS': 'Mississippi', 'MO': 'Missouri', 'MT': 'Montana', 'NE': 'Nebraska','NV': 'Nevada', 'NH': 'New Hampshire', 'NJ': 'New Jersey', 'NM': 'New Mexico','NY': 'New York', 'NC': 'North Carolina', 'ND': 'North Dakota', 'OH': 'Ohio','OK': 'Oklahoma', 'OR': 'Oregon', 'PA': 'Pennsylvania', 'RI': 'Rhode Island','SC': 'South Carolina', 'SD': 'South Dakota', 'TN': 'Tennessee', 'TX': 'Texas','UT': 'Utah', 'VT': 'Vermont', 'VA': 'Virginia', 'WA': 'Washington','WV': 'West Virginia', 'WI': 'Wisconsin', 'WY': 'Wyoming'
}

def fetch_data(industry_key):
    df = pd.read_csv("final.csv")

    # removing the null/empty obs
    df = df.dropna(subset=['date', 'value_empindustry', 'value_nonfarmemp', 'id', 'state'])

    df['date'] = pd.to_datetime(df['date'], errors='coerce')
    df['value_empindustry'] = pd.to_numeric(df['value_empindustry'], errors='coerce')
    df['value_nonfarmemp'] = pd.to_numeric(df['value_nonfarmemp'], errors='coerce')
    df['value'] = df['value_empindustry'] / df['value_nonfarmemp']

    df = df[df['id'] == series_identifiers[industry_key]]
    #mapping states
    df['state_code'] = df['state']
    df['state'] = df['state_code'].map(state_code_to_name)

    return df.dropna(subset=['value', 'state_code', 'date'])

#managing last available date from dataset 
try:
    last_date = fetch_data("Construction")['date'].max()
except Exception:
    last_date = pd.Timestamp("2000-01-01")

layout = html.Div([
    html.H2("US Employment by Industry, adjust against Non-Farm working population  (in 1000s)"),
    html.H4("Please select an Industry and the time period. The graph below defaults to the last available year-month combination for the 'Construction' Industry Category"),
    html.Br(),
    html.P('The graph below is an amalgamation of multiple datasets, outlining the factor of the number of employees working across 11 industries, against the overall Non-Farm/Agriculture working population'),
    html.Label("Select Industry"),
    html.Br(),
    dcc.Dropdown(
        id="industry_page2",
        options=[{"label": k, "value": k} for k in series_identifiers],
        value="Construction",
        clearable=False
    ),
    html.Br(),
    html.Div([
        html.Div([
            html.Label("Select Year"),
            dcc.Dropdown(id="year_page2", clearable=False, style={"width": "150px"})
        ], style={"flex": "1", "marginRight": "20px"}),
        html.Div([
            html.Label("Select Month"),
            dcc.Slider(
                id="month_page2",
                min=1,
                max=12,
                step=1,
                marks={i: m for i, m in enumerate(["Jan","Feb","Mar","Apr","May","Jun","Jul","Aug","Sep","Oct","Nov","Dec"], 1)},
                value=last_date.month,
                tooltip={"placement":"bottom","always_visible":True}
            )
        ], style={"flex": "3"})
    ], style={"display": "flex", "alignItems": "center", "marginBottom": "20px"}),
    dcc.Graph(id="choropleth_page2")
])

@callback(
    Output("year_page2", "options"),
    Output("year_page2", "value"),
    Output("choropleth_page2", "figure"),
    Input("industry_page2", "value"),
    Input("year_page2", "value"),
    Input("month_page2", "value")
)
def update_dropdown_and_map(industry, selected_year, selected_month):
    df = fetch_data(industry)
    if df.empty:
        return [], None, px.choropleth(title="No Data Available")

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
        return year_options, selected_year, px.choropleth(title="No Data Available for Selected Date")

    fig = px.choropleth(
        filtered_df,
        locations="state_code",
        locationmode="USA-states",
        scope="usa",
        color="value",
        hover_name="state",
        color_continuous_scale="Viridis",
        title=f"{industry} Employment - {pd.Timestamp(selected_year, selected_month, 1).strftime('%B %Y')}"
    )

    return year_options, selected_year, fig
