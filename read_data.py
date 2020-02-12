import pandas as pd

def str_month2int_month(month):
    month_dictionary = {'JAN':1,'FEB':2,'MAR':3,'APR':4,'MAY':5,'JUN':6,'JUL':7,'AUG':8,'SEP':9,'OCT':10,'NOV':11,'DEC':12} 
    value = month_dictionary[month]
    return value


file = r'CTA-Ridership-L-Station-Entries-Daily_totals.csv'

df = pd.read_csv(file, low_memory=False)

header_list = list(df)         # to get the header of file as list

station_id = df['station_id']
station_name = df['stationname']
date = df['date']
daytype = df['daytype']
rides = df['rides']

