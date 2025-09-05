'''
1. Team 13 : Jackson Shelton, Justin Varela, Pranav Prathap, Yixuan Tan

2. Question / Story : to what extent have states historically been proactive about raising their minimum wage? This could provoke further study into why some states may be more proactive than others due to social or political factors. We wanted to see how states have proactively raised their minimum wage above the federal rate over time.

3. Data choices: We used the state minimum wages of Texas, Virginia, Illinois, California, and New York adjusted down by the federal minimum wage. The state selection encompasses that are considered pro-active and others that may not be. There is also a unionized v. not-unionized element to the different states. 

4. Takeaways: From 1968 to 2000, most states did not raise their minimum wage above the federal rate proactively.
Beginning in 2000, a few states raised their rates marginally above the federal rate but were brought closer to the federal rate when it was raised in 2007-2009.
Post 2009, the federal rate stagnated and most states began to raise their rates well above the federal rate, but Texas has notably never raised their minimum wage above the federal rate potentially indicating strong social or political opposition.
'''
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~ #

'''
AI Assistance : (Also marked using in-line comments)

Plotting specifically at the end of each line 
    ending_mw,end_loc = df['value_y'].iloc[-1],df['date'].iloc[-1] ## FROM GPT

Adding an offset to the labels to avoid overlapping of plot values
    y_offset = 0.1

'''

# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~ #

import requests # Handles request methods when using API endpoints as the data acquisition source
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import json
from dash import Dash, html # Handles dashboard creation
from datetime import datetime # to manage date & time functionality 

## From the list of available FRED APIs, we chose to use the series/observations endpoint to deliver the datasets. Other endpoints used were 'category/series' and '/series' to provide the list of available datasets and the metadata of individual ones.
url = 'https://api.stlouisfed.org/fred/series/observations'

# Initializing and declaring environment variables
fred_api_key = '1d90de899e9698a2924f22d85c093fe6'
series_identifiers = ['STTMINWGNY','STTMINWGTX','STTMINWGIL','STTMINWGVA','STTMINWGCA']
state_labels = ['New York','Texas','Illinois','Virginia','California']
line_colors = ['#f3c331','#f8955c','#f0484e','#7e5f02','#99215b']

#fetching and storing federal data to use as the baseline 
params = {'series_id': 'STTMINWGFG', ##This is the ID to the Dataset for the Federal Data. 
        'api_key': fred_api_key,
        'file_type':'json'}
response = requests.get(url,params = params)
if response.status_code == 200:
  data = response.json()
  obs = data.get('observations', [])
  df_base = pd.DataFrame(obs) 
  df_base['value'] = pd.to_numeric(df_base['value'], errors = 'coerce') # Analytical Modifications Made : Transformation
  df_base['date'] = pd.to_datetime(df_base['date'], errors = 'coerce') # Analytical Modifications Made : Transformation
  

# Plot dimensions
plt.figure(figsize = (12,6))
plt.ylim(-0.2,10)
# Fetching individual state data to then compare against the Federal minimum and plot on a Line chart. 
for count,i in enumerate(series_identifiers) :
    params = {
        'series_id': i,
        'api_key': fred_api_key,
        'file_type': 'json'
        }
    
    response = requests.get(url, params=params) # GET method used to call FRED

    '''# to test endpoint response
    if response.status_code == 200:
        data = response.json()
        print(json.dumps(data,indent=4))
    else:
        print("Error:", response.status_code, response.text)'''

    if response.status_code == 200: # Successful Request, all other codes indicated error in payload/server-side
        data = response.json()
        obs = data.get('observations', [])
        df = pd.DataFrame(obs)
        df['value'] = pd.to_numeric(df['value'],errors='coerce') 
        df['date'] = pd.to_datetime(df['date'],errors='coerce')
        df = pd.merge(df_base, df, on = 'date', how = 'left' )
        df.fillna(0, inplace = True)
        #print(df)
        df['value_y'] = df['value_y']-df_base['value']
        df['value_y'][df['value_y']<0] = 0  # keeping values only if above federal
       
        plt.plot(df['date'], df['value_y'], linestyle='-',color = line_colors[count],label=state_labels[count],marker='.')
            
        #df['value'] = df['value'] * 100
        #print(df.head())

        ending_mw,end_loc = df['value_y'].iloc[-1],df['date'].iloc[-1] ## FROM GPT

        y_offset = 0.1 # vertical shift to avoid overlap ~~ FROM GPT
        plt.text(end_loc, ending_mw + count * y_offset, f"{ending_mw:.2f}",fontsize=8,color = line_colors[count], ha='left', va='bottom')

    else:
        print('Error:', response.status_code, response.text)

plt.title(f'State-Wise Minimum Wage Rates of Select States Above the Federal Minimum: (1968 to 2025)')
plt.xlabel('Year')
plt.ylabel('Minimum Wage Above the Federal Minimum (USD)')
plt.grid(True)
plt.annotate('Source: FRED', xy = (-1,1.5))
plt.annotate('Baseline on the y-axis at 0 is the federal minimum wage', xy = (-1,1))
plt.legend()
plt.savefig(f'assets/Wage_graph.png')


# Creating the dash app

app = Dash(__name__)
app.title = 'State Minimum Wages'

app.layout = html.Div([
    html.H1('Analysis of State-wise Minimum wage trends', style={ 'border-bottom': 'grey' 'solid' '0.5px','padding-bottom': '25px'}),
    html.H4('Team 13 : '),
    html.H4('Jack Shelton, Justin Varela, Yixuan Tan, Pranav Prathap', style={'font-style':'italic'}),
    html.Br(),
    html.Br(),
    html.H3('Objective and Approach'),
    html.P('We wanted to see how states have proactively raised their minimum wage above the federal rate over time. To do this, we took the minimum wage annually for each selected state and then adjusted it down by the federal minimum wage and plotted it on the graph below.'),
    html.Img(src=f'assets/Wage_graph.png'),
    html.H3('Observations'),
    html.P('For most of the history of the minimum wage, states defaulted to the Federal rate. States did not begin proactively raising their minimum wage until around 2000 with California being the first to act. The state minimums increasingly outpaced the Federal minimum towards the end of the series as the Federal rate has not been raised since 2009. New York and California were the highest, potentially reflecting higher costs of living or a stronger labor presence politically. The only state to not see an increase is Texas which in fact has never raised their minimum wage above the Federal rate despite its stagnation and increased costs of living. This potentially indicates some social or political resistance to the raising of the minimum wage or the minimum wage itself.'),
], className='Divstyle'
)


#Running the app
if __name__ == "__main__":
   app.run(debug = True, use_reloader = False)