# CTBA_Final_Team13
Industry Employment Statistics Dashboard:
Team 13
Collaborators: Jackson Shelton, Justin, Pranav Prathap

Purpose:
The idea behind the dashboard is to provide a general overview of employment statistics by industry. The intended use is to be able to identify sudden events and trends within the employment data which could be avenues for further research. The other intended use is for users to be able to see the statistical impact of events or trend within an industry that they have already identified. To this end we included three interactive visualizations:

1. Employee counts by industry over time: 
   This time series is customizable to show the industries that the user selects on the Checkbox. The data is sourced from the FRED total employee counts for the given named industries. The range of the time series is also customizable using the date range selector. A toggle to show the FRED GDP-based recession indicator is also included as recessions commonly impact employment depending on the industry.

2. Employee counts by industry by state:
   This Choropleth shows the employee counts by state for the selected industry. One industry may be selected at a time, and the employee counts are expressed as a percentage of total non-farm jobs within the state to avoid overrepresenting more populous states in the choropleth.

3. Average hourly wage by industry over time:
   This time series is customizable to show the industries that the user selects on the checkbox. THe data is sourced from the FRED average hourly wage for non-supervisory employees for given industry. Non-supervisory employees were used because the dataset goes back far further, and we wanted to focus the analysis on production-oriented employees that make up the bulk of the workforce in the industries.

How to Run:
The 'final' csv is required to run the dashboard. The other datasets are sourced using the FRED API, but the amount of requests required to build the employment by state and industry dataframe made the application too slow. The csv should be included in the zip file. The three page files within the pages folder are also required. As long as the full zip file has been downloaded, unzipped, and unaltered, all that should be required to run the file is to run the app.py file.

Data Sources:
Page One: FRED ID: 'USMINE', 'USCONS', 'MANEMP', 'USTPU','USINFO', 'USFIRE', 'USPBS', 'USEHS', 'USLAH', 'USSERV', 'USGOVT', 'JHGDPBRINDX'
Page Two: FRED ID: Every combination of state code and the following IDs: 'NRMN', 'CONS'
, 'MFG', 'TRAD', 'INFO', 'FIRE', 'PBSV', 'EDUH', 'LEIH', 'SRVO', 'GOVT'

Page Three: FRED ID: 'CES1000000008', 'CES2000000008', 'CES3000000008', 'CES4000000008','CES5000000008', 'CES5500000008', 'CES6000000008', 'CES6500000008', 'CES7000000008', 'CES8000000008', 'CPIAUCSL'
