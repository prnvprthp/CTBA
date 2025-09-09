from dash import html, dcc, Input, Output, register_page, callback
import pandas as pd
import requests
import numpy as np
import plotly.express as px
import datetime

state_dict = {'Alabama': 'AL','Alaska': 'AK','Arizona': 'AZ','Arkansas': 'AR','California': 'CA','Colorado': 'CO','Connecticut': 'CT','Delaware': 'DE','Florida': 'FL','Georgia': 'GA','Hawaii': 'HI','Idaho': 'ID','Illinois': 'IL','Indiana':'IN','Iowa': 'IA','Kansas': 'KS','Kentucky': 'KY','Louisiana': 'LA','Maine': 'ME','Maryland': 'MD','Massachusetts': 'MA','Michigan': 'MI','Minnesota': 'MN','Mississippi': 'MS','Missouri': 'MO','Montana': 'MT','Nebraska': 'NE','Nevada': 'NV','New Hampshire': 'NH','New Jersey': 'NJ','New Mexico': 'NM','New York': 'NY','North Carolina': 'NC','North Dakota': 'ND','Ohio': 'OH','Oklahoma': 'OK','Oregon': 'OR','Pennsylvania': 'PA','Rhode Island': 'RI','South Carolina': 'SC','South Dakota': 'SD','Tennessee': 'TN','Texas': 'TX','Utah': 'UT','Vermont': 'VT','Virginia': 'VA','Washington': 'WA','West Virginia': 'WV','Wisconsin': 'WI','Wyoming': 'WY','District of Columbia': 'DC'}
series_identifiers = {'Non Farm Emp':'NA'}

fred_api_key = '1d90de899e9698a2924f22d85c093fe6'
url = 'https://api.stlouisfed.org/fred/series/observations'

df = pd.DataFrame(columns=['date', 'value', 'id','state'])

for i in state_dict.values():
    for j in series_identifiers.values():
        params = {
            "series_id": i + j,
            "api_key": fred_api_key,
            "file_type": "json"
        }
        response = requests.get(url, params=params)

        if response.status_code == 200:
            data = response.json()
            obs = data.get("observations", [])
            temp = pd.DataFrame(obs)[['date','value']]
            temp["date"] = pd.to_datetime(temp["date"], errors="coerce")
            temp["value"] = pd.to_numeric(temp["value"], errors="coerce")
            temp["id"] = i + j
            temp['state'] = i
            df = pd.concat([df, temp], ignore_index=True)
        else:
            # If the request fails, append a row with NaNs
            temp = pd.DataFrame([{
                "date": pd.NaT,
                "value": np.nan,
                "id": i + j
            }])
            df = pd.concat([df, temp], ignore_index=True)

print(df.head())

df.to_csv('statenonfarmemp.csv',index=False)

#merging the tables
# Load
empindustry = pd.read_csv("Empbystateindustry.csv")
nonfarmemp = pd.read_csv("statenonfarmemp.csv")

# Rename values
empindustry = empindustry.rename(columns={"value": "value_empindustry"})
nonfarmemp = nonfarmemp.rename(columns={"value": "value_nonfarmemp"})

# Normalize merge keys
empindustry["date"] = pd.to_datetime(empindustry["date"], errors="coerce")
nonfarmemp["date"] = pd.to_datetime(nonfarmemp["date"], errors="coerce")

empindustry["state"] = empindustry["state"].str.strip()
nonfarmemp["state"] = nonfarmemp["state"].str.strip()

# Merge
merged = pd.merge(empindustry, nonfarmemp[["date", "state", "value_nonfarmemp"]],on=["date", "state"], how="left")
merged['id'] = merged['id'].str[2:]

merged.to_csv("final.csv", index=False)
