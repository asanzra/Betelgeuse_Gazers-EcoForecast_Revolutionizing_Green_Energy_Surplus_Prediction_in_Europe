import argparse
import csv
import os
import pandas as pd
from datetime import datetime, timedelta, timezone

basic_info = True
extra_info = False

REGIONS = {
    'HU': '10YHU-MAVIR----U',
    'IT': '10YIT-GRTN-----B',
    'PO': '10YPL-AREA-----S',
    'SP': '10YES-REE------0',
    'UK': '10Y1001A1001A92E',
    'DE': '10Y1001A1001A83F',
    'DK': '10Y1001A1001A65H',
    'SE': '10YSE-1--------K',
    'NE': '10YNL----------L',
}
#We do not consider as green and renewable: B01 Biomass, B02-B08 Fossils, B17 Waste
GREEN_ENERGIES = {
    'B09' : 'Geothermal',
    'B10' : 'Hydro Pumped Storage',
    'B11' : 'Hydro Run-of-river and poundage',
    'B12' : 'Hydro Water Reservoir',
    'B13' : 'Marine',
    'B14' : 'Nuclear',
    'B15' : 'Other renewable',
    'B16' : 'Solar',
    'B18' : 'Wind Offshore',
    'B19' : 'Wind Onshore'
}
LOAD='Load'
#AreaID not considered relevant.
DATA_POINTS=[
    'StartTime',
    'EndTime',
    'UnitName'
]
QUANTITY='quantity'
# Create a dict containing the columns each country has.
ENERGY_CATEGORIES=GREEN_ENERGIES.copy()
ENERGY_CATEGORIES[LOAD]=LOAD

# Checks if a date is in expected format
def is_expected_date_format(date_string):
    try:
        # Attempt to parse the date string
        datetime.strptime(date_string, "%Y-%m-%dT%H:%M%zZ")
        return True
    except ValueError:
        return False

def load_data(file_path):
    # TODO: Load data from CSV file
    data={}
    for COUNTRY in REGIONS:
        if basic_info:
            print(f'Loading country: {COUNTRY}...')
        if extra_info:
            print(f'Doing load for country: {COUNTRY}')
        data[COUNTRY]={} #Create a dictionary for each country
        data[COUNTRY][LOAD]=[] #Create an empty list for the load data
        load_path=f'./data/load_{COUNTRY}.csv'
        if os.path.isfile(load_path):
            with open(load_path, newline='') as csvfile: #Open load csv file
                reader = csv.DictReader(csvfile) #Create a reader for it
                for row in reader:
                    if row['AreaID']!=REGIONS[COUNTRY]:#ELIMINATES BLANK CODE DATA
                            break
                    dicti = {} #Store all data in a dict
                    for DATA_POINT in DATA_POINTS:
                        dicti[DATA_POINT] = row[DATA_POINT] #Store relevant vaiables: dates, units...
                        if DATA_POINT == 'StartTime' or DATA_POINT == 'EndTime':
                            if not is_expected_date_format(dicti[DATA_POINT]):
                                raise Exception("One data point does not have correct form of timezone")
                            #Remove timezone info
                            dicti[DATA_POINT]=datetime.strptime(dicti[DATA_POINT][:-1], "%Y-%m-%dT%H:%M%z").strftime("%Y-%m-%d %H:%M")
                    dicti[QUANTITY] = row[LOAD]
                    # if row['AreaID']!=REGIONS[COUNTRY]:
                    #     print(f'In load, country: {COUNTRY} is taking id: {row["AreaID"]}, when it should only take {REGIONS[COUNTRY]}!')
                    data[COUNTRY][LOAD].append(dicti) #Store dict as dataframe
                data[COUNTRY][LOAD] = sorted(data[COUNTRY][LOAD], key=lambda x: x["StartTime"])
        for ENERGY in GREEN_ENERGIES:
            if extra_info:
                print(f'Doing energy: {ENERGY} for country: {COUNTRY}')
            data[COUNTRY][ENERGY]=[] #Create an empty list for each energy data
            energy_path = f'./data/gen_{COUNTRY}_{ENERGY}.csv'
            if os.path.isfile(energy_path):
                with open(energy_path, newline='') as csvfile: #Open energy csv file
                    reader = csv.DictReader(csvfile) #Create a reader for it
                    for row in reader:
                        if row['AreaID']!=REGIONS[COUNTRY]:#ELIMINATES BLANK CODE DATA
                            break
                        dicti = {} #Store all data in a dict
                        for DATA_POINT in DATA_POINTS:
                            dicti[DATA_POINT] = row[DATA_POINT] #Store relevant vaiables: dates, units...
                            if DATA_POINT == 'StartTime' or DATA_POINT == 'EndTime':
                                if not is_expected_date_format(dicti[DATA_POINT]):
                                    raise Exception("One data point does not have correct form of timezone")
                                #Remove timezone info
                                dicti[DATA_POINT]=datetime.strptime(dicti[DATA_POINT][:-1], "%Y-%m-%dT%H:%M%z").strftime("%Y-%m-%d %H:%M")
                        dicti[QUANTITY] = row[QUANTITY]
                        # if row['AreaID']!=REGIONS[COUNTRY]:
                        #     print(f'In energy:{ENERGY}, country: {COUNTRY} is taking id: {row["AreaID"]}, when it should only take {REGIONS[COUNTRY]}!')
                        data[COUNTRY][ENERGY].append(dicti) #Store dict as dataframe
                    if COUNTRY == "IT" and ENERGY=="B10":
                        print(data['IT']['B10'])
                    data[COUNTRY][ENERGY] = sorted(data[COUNTRY][ENERGY], key=lambda x: x["StartTime"])
    df=data
    print(data['IT']['B10'])
    return df

# # Define your date range
# start_date = datetime(2022, 1, 1, 0, 0)  # January 1, 2023, 00:00 (midnight)
# end_date = datetime(2023, 1, 1, 23, 59)   # January 3, 2023, 23:59

# # Define the time step
# hour_delta = timedelta(hours=1)

# # Iterate over every hour in the date range
# current_date = start_date
# while current_date <= end_date:
#     print(current_date)
#     current_date += hour_delta


def clean_data(df):
    # TODO: Handle missing values, outliers, etc.
    #First we need to only get 1h intervals
    for COUNTRY in REGIONS:
        if basic_info:
            print(f'Cleaning country: {COUNTRY}...')
        for ENERGY in ENERGY_CATEGORIES:
            if extra_info:
                print(f'Cleaning column: {ENERGY} for country: {COUNTRY}')
            for i, dicti in enumerate(df[COUNTRY][ENERGY]):
                start_datetime = datetime.strptime(dicti['StartTime'], "%Y-%m-%d %H:%M")
                new_end_datetime = datetime.strptime(dicti['EndTime'], "%Y-%m-%d %H:%M")
                time_difference = new_end_datetime - start_datetime #Delta time for this new interval
                if i != 0:
                    if end_datetime != start_datetime: #If the new start time is not the old end time
                        hours_time_difference = time_difference.total_seconds() / 3600
                        if hours_time_difference < 1:
                            #Buscar datos en esa hora y hacer media
                        else:
                            #
                        raise Exception(f'New end time not same as old start time in energy: {ENERGY} for country: {COUNTRY}'+
                                        f'\n Old end time: {end_datetime}, new start time: {start_datetime}')
                end_datetime = new_end_datetime
                if i == 0:
                    delta_time = time_difference
                else:
                    if time_difference != delta_time: #If the new delta time is not as all other delta times
                        raise Exception(f'Delta time not constant in energy: {ENERGY} for country: {COUNTRY}'+
                                        f'\n First delta time: {delta_time}, this one:{time_difference}')
                

    df_clean=None #Linea para que corra
    return df_clean

def preprocess_data(df):
    # TODO: Generate new features, transform existing features, resampling, etc.
    df_processed=None #Linea para que corra
    return df_processed

def save_data(df, output_file):
    # TODO: Save processed data to a CSV file
    pass

def parse_arguments():
    parser = argparse.ArgumentParser(description='Data processing script for Energy Forecasting Hackathon')
    parser.add_argument(
        '--input_file',
        type=str,
        default='data/raw_data.csv',
        help='Path to the raw data file to process'
    )
    parser.add_argument(
        '--output_file', 
        type=str, 
        default='data/processed_data.csv', 
        help='Path to save the processed data'
    )
    return parser.parse_args()

def main(input_file, output_file):
    df = load_data(input_file)
    df_clean = clean_data(df)
    df_processed = preprocess_data(df_clean)
    save_data(df_processed, output_file)

if __name__ == "__main__":
    args = parse_arguments()
    main(args.input_file, args.output_file)