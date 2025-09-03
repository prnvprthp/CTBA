import requests
import pandas as pd
import matplotlib.pyplot as plt
import json


url = 'https://api.stlouisfed.org/fred/series/observations'

results = []
fred_api_key = '1d90de899e9698a2924f22d85c093fe6'
dataset_identifier = 'STTMINWGOH'
params = {
    'series_id': dataset_identifier,
    'api_key': fred_api_key,
    'file_type': "json",
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
    obs = data.get('observations', [])
    df = pd.DataFrame(obs)
    df['value'] = pd.to_numeric(df['value'],errors='coerce')
    df['date'] = pd.to_datetime(df['date'],errors='coerce')
    #df['value'] = df['value'] * 100
    print(df.head())
else:
    print('Error:', response.status_code, response.text)

plt.plot(df['date'], df['value'], linestyle='-') #, marker='.'

plt.title("State Minimum Wage Rate for Ohio : 1968 to 2025")
plt.xlabel("Year")
plt.ylabel("Minimum Wage (USD)")
plt.grid(True)
plt.show()