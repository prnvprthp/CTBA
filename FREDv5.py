import requests
import pandas as pd
import matplotlib.pyplot as plt
import json


url = 'https://api.stlouisfed.org/fred/series/observations'

results = []
fred_api_key = '1d90de899e9698a2924f22d85c093fe6'
series_identifiers = ['STTMINWGNY','STTMINWGTX','STTMINWGIL','STTMINWGVA','STTMINWGCA']
state_labels = ['New York','Texas','Illinois','Virginia','California']
line_colors = ['orange','purple','green','cyan','red']

params = {'series_id': 'STTMINWGFG',
        'api_key': fred_api_key,
          'file_type':'json'}
response = requests.get(url,params = params)
if response.status_code == 200:
  data = response.json()
  print(data)
  obs = data.get('observations', [])
  df_base = pd.DataFrame(obs) 
  print(df_base.head())
  df_base['value'] = pd.to_numeric(df_base['value'], errors = 'coerce')

for count,i in enumerate(series_identifiers) :
    params = {
        'series_id': i,
        'api_key': fred_api_key,
        'file_type': "json"
        }
    

    response = requests.get(url, params=params) ## in a loop

    '''# to test endpoint response
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
        df['value'] = df['value']-df_base['value']
        df['value'][df['value']<0] = 0
      
            
        
        #df['value'] = df['value'] * 100
        #print(df.head())

        if i != series_identifiers[-1]:
            plt.plot(df['date'], df['value'], linestyle='-',color = line_colors[count],label=state_labels[count])
        else:
            plt.plot(df['date'], df['value'], linestyle='-',color = line_colors[count],label=state_labels[count])

        starting_mw,start_loc = df['value'].iloc[0],df['date'].iloc[0] ## FROM GPT
        ending_mw,end_loc = df['value'].iloc[-1],df['date'].iloc[-1] ## FROM GPT

        y_offset = 0.4  # vertical shift to avoid overlap ~~ FROM GPT
        plt.text(start_loc, starting_mw + count * y_offset, f"{starting_mw:.2f}",fontsize=8, color=line_colors[count],ha='right', va='bottom')
        plt.text(end_loc, ending_mw + count * y_offset, f"{ending_mw:.2f}",fontsize=8,color = line_colors[count], ha='left', va='bottom')

    else:
        print('Error:', response.status_code, response.text)

plt.title(f"State-Wise Minimum Wage Rates of {', '.join(state_labels[0:-1])} above the federal minimum: (1968 to 2025)")
plt.xlabel("Year")
plt.ylabel("Minimum Wage (USD)")
plt.grid(True)
plt.legend()
plt.show()