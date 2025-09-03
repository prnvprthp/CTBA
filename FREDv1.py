import requests
import pandas as pd
import matplotlib.pyplot as plt
import json


url = "https://api.stlouisfed.org/fred/series/observations"

results = []
fred_api_key = '1d90de899e9698a2924f22d85c093fe6'

params = {
    "series_id": "STTMINWGOH",
    "api_key": fred_api_key,
    "file_type": "json",
}

response = requests.get(url, params=params)

'''# checking endpoint response
if response.status_code == 200:
    data = response.json()
    print(json.dumps(data,indent=4))
else:
    print("Error:", response.status_code, response.text)'''

if response.status_code == 200:
    data = response.json()
    obs = data.get("observations", [])
    df = pd.DataFrame(obs)
    print(df.head())
else:
    print("Error:", response.status_code, response.text)