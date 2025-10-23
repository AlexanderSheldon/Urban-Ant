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
    print(data['tables'][tableID]['title'], "Table ID:", tableID)

    if print_cols == True:
        # Print the columns names and IDs in the table
        for col in data['tables'][tableID]['columns']:
            print('\t', data['tables'][tableID]['columns'][col]['name'],'\tColumn ID:', col)


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

table_ids = ['B08301','B01002','B08303','B08201','B08134']

# for table in table_ids:
    # table_info(table, print_cols=True)

table_info("B08134", print_cols=True)
'''

"Total Travel Time to Work via Public transportation" : ('B08134', 'B08134061'),
"Less than 10 minutes Travel Time to Work via Public transportation" : ('B08134','B08134062'),
"10 to 14 minutes Travel Time to Work via Public transportation" : ('B08134','B08134063'),
"15 to 19 minutes Travel Time to Work via Public transportation" : ('B08134','B08134064'),
"20 to 24 minutes Travel Time to Work via Public transportation" : ('B08134','B08134065'),
"25 to 29 minutes Travel Time to Work via Public transportation" : ('B08134','B08134066'),
"30 to 34 minutes Travel Time to Work via Public transportation" : ('B08134','B08134067'),
"35 to 44 minutes Travel Time to Work via Public transportation" : ('B08134','B08134068'),
"45 to 59 minutes Travel Time to Work via Public transportation" : ('B08134','B08134069'),
"60 or more minutes Travel Time to Work via Public transportation" : ('B08134','B08134070'),
"Total Travel Time to Work via Driving Alone" : ('B08134','B08134021'),
"Less than 10 minutes Travel Time to Work via Driving Alone" : ('B08134','B08134022'),
"10 to 14 minutes Travel Time to Work via Driving Alone" : ('B08134','B08134023'),
"15 to 19 minutes Travel Time to Work via Driving Alone" : ('B08134','B08134024'),
"20 to 24 minutes Travel Time to Work via Driving Alone" : ('B08134','B08134025'),
"25 to 29 minutes Travel Time to Work via Driving Alone" : ('B08134','B08134026'),
"30 to 34 minutes Travel Time to Work via Driving Alone" : ('B08134','B08134027'),
"35 to 44 minutes Travel Time to Work via Driving Alone" : ('B08134','B08134028'),
"45 to 59 minutes Travel Time to Work via Driving Alone" : ('B08134','B08134029'),
"60 or more minutes Travel Time to Work via Driving Alone" : ('B08134','B08134030')

'''
