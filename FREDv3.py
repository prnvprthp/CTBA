import requests
import pandas as pd
import matplotlib.pyplot as plt
import json


url = 'https://api.stlouisfed.org/fred/series/observations'

results = []
fred_api_key = '1d90de899e9698a2924f22d85c093fe6'
dataset_identifier1 = 'STTMINWGOH'
series = ['STTMINWGOH','STTMINWGTX','STTMINWGMA','STTMINWGVA']
for i in series:
    params = {
        'series_id': i,
        'api_key': fred_api_key,
        'file_type': "json",
    }

response1 = requests.get(url, params=params) ## in a loop

'''# checking endpoint response
if response.status_code == 200:
    data = response.json()
    print(json.dumps(data,indent=4))
else:
    print("Error:", response.status_code, response.text)'''

if response1.status_code == 200:
    data = response1.json()
    obs = data.get('observations', [])
    df = pd.DataFrame(obs)
    df['value'] = pd.to_numeric(df['value'],errors='coerce')
    df['date'] = pd.to_datetime(df['date'],errors='coerce')
    #df['value'] = df['value'] * 100
    print(df.head())
else:
    print('Error:', response1.status_code, response1.text)

plt.plot(df['date'], df['value'], linestyle='-') #, marker='.'

plt.title("State Minimum Wage Rate for Ohio : 1968 to 2025")
plt.xlabel("Year")
plt.ylabel("Minimum Wage (USD)")
plt.grid(True)
plt.show()


dataset_identifier2 = 'STTMINWGTX'
params2 = {
    'series_id': dataset_identifier2,
    'api_key': fred_api_key,
    'file_type': "json",
}

########

response2 = requests.get(url, params=params2)

'''# checking endpoint response
if response.status_code == 200:
    data = response.json()
    print(json.dumps(data,indent=4))
else:
    print("Error:", response.status_code, response.text)'''

if response1.status_code == 200:
    data = response2.json()
    obs = data.get('observations', [])
    df = pd.DataFrame(obs)
    df['value'] = pd.to_numeric(df['value'],errors='coerce')
    df['date'] = pd.to_datetime(df['date'],errors='coerce')
    #df['value'] = df['value'] * 100
    print(df.head())
else:
    print('Error:', response1.status_code, response1.text)

plt.plot(df['date'], df['value'], linestyle='-') #, marker='.'

plt.title("State Minimum Wage Rate for Texas : 1968 to 2025")
plt.xlabel("Year")
plt.ylabel("Minimum Wage (USD)")
plt.grid(True)
plt.show()

## ~~~ for v4 ~~~ 
# Add plot to dash

# NY(unionized), TX(right to work), IL, VA, FL(right to work)
# vs. Federal Minimum Wage (use as normal)
# difference b/w the state and federal
