import pandas as pd
import json
import requests


def table_info(tableID, print_cols=False):
    # Connect to API
    geoID = '14000US01097001001' # Base GeoID (1st census tract) change later to incorporate more, or don't

    API_url = f'https://api.censusreporter.org/1.0/data/show/latest?table_ids={tableID}&geo_ids={geoID}'

    r = requests.get(API_url)
    r.raise_for_status()                # raise if HTTP error (4xx/5xx)
    data = r.json()                     # parse JSON

    
    
    # Print the title of the table
    print(data['tables'][tableID]['title'])

    if print_cols == True:
        # Print the columns names and IDs in the table
        for col in data['tables'][tableID]['columns']:
            print(data['tables'][tableID]['columns'][col]['name'],'\tColumn ID:', col)


'''
Population & households

B01003 Total population

B11001 Households

Income / poverty / education

B19013 Median household income

B17001 Poverty status by sex by age (use for % below poverty line)

B15003 Educational attainment (25+)

Commuting & access

B08301 Means of transportation to work (look for columns with “Public transportation”)

B08303 Travel time to work

B08201 Households by vehicles available (also see B25044 Tenure × vehicles)

Housing

B25003 Tenure (owner/renter)

B25064 Median gross rent

B25077 Median home value
'''

table_ids = ['B08301','B08303','B08201']

for table in table_ids:
    table_info(table, print_cols=False)