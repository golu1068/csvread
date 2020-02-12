import pandas as pd


file = r'CTA-Ridership-L-Station-Entries-Daily_totals.csv'

df = pd.read_csv(file, low_memory=False)

header_list = list(df)         # to get the header of file as list

station_id = df['station_id']
station_name = df['stationname']
date = df['date']
daytype = df['daytype']
rides = df['rides']

