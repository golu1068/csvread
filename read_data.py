import pandas as pd
import datetime
import calendar

file = r'E:\download\CTA_-_Ridership_-__L__Station_Entries_-_Daily_Totals.csv'

li=[];new_date=[];
all_data={};


df = pd.read_csv(file, low_memory=False)

header_list = list(df)         # to get the header of file as list

station_id = df['station_id']
station_name = df['stationname']
date = df['date']
daytype = df['daytype']
rides = df['rides']

for i in range(len(station_id)):
    try:
        month = int(date[i][0:2])
        day = int(date[i][3:5])
        year = int(date[i][6:10])
        new_date[0:0] = [month, day, year]
        li[0:0] = [station_name[i], new_date, daytype[i], rides[i]]
        all_data[station_id[i]] = li
        new_date=[];
        li=[];
    except:
        print(i, station_id[i], date[i])
        raise
print(all_data)
