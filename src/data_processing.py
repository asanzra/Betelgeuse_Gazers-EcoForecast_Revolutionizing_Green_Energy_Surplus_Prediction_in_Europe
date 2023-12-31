import argparse
import csv
import os
import pandas as pd
from datetime import datetime, timedelta, timezone
import numpy as np
import matplotlib.pyplot as plt

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
    'NE': '10YNL----------L'
}
COUNTRY_IDS={
    'SP': 0, # Spain
    'UK': 1, # United Kingdom
    'DE': 2, # Germany
    'DK': 3, # Denmark
    'HU': 5, # Hungary
    'SE': 4, # Sweden
    'IT': 6, # Italy
    'PO': 7, # Poland
    'NL': 8 # Netherlands
}
#We do not consider as green and renewable: B01 Biomass, B02-B08 Fossils, B17 Waste
GREEN_ENERGIES = {
    'B01' : 'Biowaste',
    'B09' : 'Geothermal',
    'B10' : 'Hydro Pumped Storage',
    'B11' : 'Hydro Run-of-river and poundage',
    'B12' : 'Hydro Water Reservoir',
    'B13' : 'Marine',
    'B15' : 'Other renewable',
    'B16' : 'Solar',
    'B18' : 'Wind Offshore',
    'B19' : 'Wind Onshore'
}
LOAD='Load'
#AreaID not considered relevant, as well as UnitName as all are MAW.
DATA_POINTS=[
    'StartTime',
    'EndTime'
]
QUANTITY='quantity'
# Create a dict containing the columns each country has.
ENERGY_CATEGORIES=GREEN_ENERGIES.copy()
ENERGY_CATEGORIES[LOAD]=LOAD

COUNTRIES = {
    'HU': 'Hungary',
    'IT': 'Italy',
    'PO': 'Poland',
    'SP': 'Spain',
    'UK': 'United Kingdom',
    'DE': 'Germay',
    'DK': 'Denmark',
    'SE': 'Sweden',
    'NE': 'Netherlands',
}

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
                    if row['UnitName']!='MAW':
                        raise Exception('One unit name is not MAW but: {row["UnitName"]}')
                    dicti = {} #Store all data in a dict
                    for DATA_POINT in DATA_POINTS:
                        dicti[DATA_POINT] = row[DATA_POINT] #Store relevant vaiables: dates, units...
                        if DATA_POINT == 'StartTime' or DATA_POINT == 'EndTime':
                            if not is_expected_date_format(dicti[DATA_POINT]):
                                raise Exception("One data point does not have correct form of timezone")
                            #Remove timezone info
                            dicti[DATA_POINT]=datetime.strptime(dicti[DATA_POINT][:-1], "%Y-%m-%dT%H:%M%z").strftime("%Y-%m-%d %H:%M")
                    dicti[QUANTITY] = int(row[LOAD])
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
                        if row['UnitName']!='MAW':
                            raise Exception('One unit name is not MAW but: {row["UnitName"]}')
                        dicti = {} #Store all data in a dict
                        for DATA_POINT in DATA_POINTS:
                            dicti[DATA_POINT] = row[DATA_POINT] #Store relevant vaiables: dates, units...
                            if DATA_POINT == 'StartTime' or DATA_POINT == 'EndTime':
                                if not is_expected_date_format(dicti[DATA_POINT]):
                                    raise Exception("One data point does not have correct form of timezone")
                                #Remove timezone info
                                dicti[DATA_POINT]=datetime.strptime(dicti[DATA_POINT][:-1], "%Y-%m-%dT%H:%M%z").strftime("%Y-%m-%d %H:%M")
                        dicti[QUANTITY] = int(row[QUANTITY])
                        # if row['AreaID']!=REGIONS[COUNTRY]:
                        #     print(f'In energy:{ENERGY}, country: {COUNTRY} is taking id: {row["AreaID"]}, when it should only take {REGIONS[COUNTRY]}!')
                        data[COUNTRY][ENERGY].append(dicti) #Store dict as dataframe
                    data[COUNTRY][ENERGY] = sorted(data[COUNTRY][ENERGY], key=lambda x: x["StartTime"])
    df=data
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


def get_exact_hour(hour_datetime):
    hour={
        'year' : hour_datetime.year,
        'month' : hour_datetime.month,
        'day' : hour_datetime.day,
        'hour' : hour_datetime.hour
        }   
    return f'{hour["year"]}-{hour["month"]}-{hour["day"]} {hour["hour"]}'

def has_duplicates(lst):
    return len(lst) != len(set(lst))

def clean_data(df):
    # TODO: Handle missing values, outliers, etc.
    #First we need to only get 1h intervals
    df_clean={}
    for COUNTRY in REGIONS:
        if basic_info:
            print(f'Cleaning country: {COUNTRY}...')
        for ENERGY in ENERGY_CATEGORIES:
            if extra_info:
                print(f'Cleaning column: {ENERGY} for country: {COUNTRY}')

            #Substitute data saved grouping it by same start hour
            data_in_each_start_hour={}
            for dicti in df[COUNTRY][ENERGY]:
                start_datetime = datetime.strptime(dicti['StartTime'], "%Y-%m-%d %H:%M")
                end_datetime = datetime.strptime(dicti['EndTime'], "%Y-%m-%d %H:%M")
                time_difference = end_datetime - start_datetime #Delta time for this new interval
                minutes = round(time_difference.total_seconds() / 60)
                if minutes != 15 and minutes != 30 and minutes != 60: #if minute interval is not 15,30 or 60
                    raise Exception('One time interval is not 15, 30 or 60 minutes but: {minutes}')
                start_hour=get_exact_hour(start_datetime)
                end_hour=get_exact_hour(end_datetime)
                if start_hour != end_hour and end_datetime.minute != 0 : #if data spans over several hours and not to exactlt next hour
                    raise Exception('Interval spans over different hours and last time is: {end_datetime.strftime("%Y-%m-%d %H:%M:%S")}')
                dicti['StartTime']=start_datetime
                dicti['EndTime']=end_datetime
                dicti['difference']=time_difference
                if not start_hour in data_in_each_start_hour: #if a list for this hour exists
                    data_in_each_start_hour[start_hour] = [dicti] #create list containing data in this hour
                else:
                    data_in_each_start_hour[start_hour].append(dicti) #append to list
            df[COUNTRY][ENERGY]=[]
            #Manage each hour, do averages or complete data
            for start_hour, hour_data in data_in_each_start_hour.items():
                start_times = [minute_data['StartTime'] for minute_data in hour_data]
                if has_duplicates(start_times):
                    raise Exception(f'Two start times are the same for this list of start times: {[dt.strftime("%Y-%m-%d %H:%M") for dt in start_times]}')
                end_times = [minute_data['EndTime'] for minute_data in hour_data]
                if has_duplicates(end_times):
                    raise Exception(f'Two end times are the same for this list of end times: {[dt.strftime("%Y-%m-%d %H:%M") for dt in end_times]}')
                second_differences = [minute_data['difference'].total_seconds() for minute_data in hour_data]
                quantities = [minute_data['quantity'] for minute_data in hour_data]
                total_second_difference = 0
                for second_difference in second_differences:
                    total_second_difference+=second_difference
                if total_second_difference > 3600: #If the sum of intervals is greater than an hour
                    raise Exception(f'Total second difference that should be max. 3600s is: {total_second_difference}s.')
                #Calculate weighted average
                average_quantity = 0
                for i, quantity in enumerate(quantities):
                    average_quantity += quantity + second_differences[i]/total_second_difference
                hour=start_hour
                df[COUNTRY][ENERGY].append({hour : average_quantity})
            df_clean[f'{COUNTRY}_{ENERGY}']=df[COUNTRY][ENERGY] #Append the list of all hours to clean data
    return df_clean

def preprocess_data(df):
    # TODO: Generate new features, transform existing features, resampling, etc.
    data_for_dataframe = {}
    for main_key, small_key_value_list in df.items():
        for small_key_value in small_key_value_list:
            small_key, value = list(small_key_value.items())[0]
            if small_key not in data_for_dataframe:
                data_for_dataframe[small_key] = {}
            data_for_dataframe[small_key][main_key] = value

    # Create a DataFrame from the organized data
    df = pd.DataFrame(data_for_dataframe)

    # Transpose the DataFrame to have main_keys as columns and small_keys as index
    df = df.transpose()

    # Remove columns and rows

    # Set the threshold for non-null values
    threshold = 5  # More than 5 NaN values
    # Identify columns to drop
    columns_to_drop = df.columns[df.isnull().sum() > threshold]





    # Create a Matplotlib Figure and Axes
    fig, ax = plt.subplots()
    fig.set_facecolor('#2c3e50')  # Set the background color to a dark color

    # Use Pandas plot on the specified Axes with a dark color scheme
    df.isnull().sum().plot(kind='bar', color='#3498db', ax=ax)  # Use a dark blue color

    # Add labels and title
    ax.set_xlabel('Energy type', color='white')
    ax.set_ylabel('Missing values', color='white')
    ax.set_title('Missing values by energy type', color='white')
    # Set the tick labels to white
    ax.tick_params(axis='x', colors='white')
    ax.tick_params(axis='y', colors='white')
    # Save the plot to a PNG file
    plt.savefig('data/missing_values_energy_plot.png')

    # Clear the plot
    plt.clf()

    # Create a Matplotlib Figure and Axes
    fig, ax = plt.subplots()
    fig.set_facecolor('#2c3e50')  # Set the background color to a dark color

    # Use Pandas plot on the specified Axes with a dark color scheme
    df.isnull().sum(axis=1).plot(kind='bar', color='#3498db', ax=ax)  # Use a dark blue color
    # Add labels and title
    ax.set_xlabel('Date', color='white')
    ax.set_ylabel('Missing values', color='white')
    ax.set_title('Missing values by date', color='white')
    # Set the tick labels to white
    ax.tick_params(axis='x', colors='white')
    ax.tick_params(axis='y', colors='white')
    # Save the plot to a PNG file
    plt.savefig('data/missing_values_time_plot.png')





    # Print the titles and number of NaN values for dropped columns
    for column in columns_to_drop:
        num_nans = df[column].isnull().sum()
        print(f"Dropped column '{column}' with {num_nans} NaN values")

    # Drop columns where the number of non-null values is less than the threshold
    df_filtered = df.drop(columns=columns_to_drop)

    # Identify rows with any NaN values
    rows_to_drop = df_filtered[df_filtered.isnull().any(axis=1)].index

    # Print the indices (or any identifier) and number of NaN values for dropped rows
    for row in rows_to_drop:
        num_nans_row = df_filtered.loc[row].isnull().sum()
        print(f"Dropped row '{row}' with {num_nans_row} NaN values")

    # Drop rows with any NaN values
    df_filtered_no_nan = df_filtered.dropna()

    labels=[]
    for index, row in df_filtered_no_nan.iterrows():
        surpluses={}
        print(f"Row: {index}")
        for i, REGION in enumerate(REGIONS):
            country_columns = row.filter(regex=f'^{REGION}_')
            if country_columns.empty:
                continue
            green_totals = 0
            for GREEN_ENERGY in GREEN_ENERGIES:
                green_column = country_columns.filter(regex=f'{GREEN_ENERGY}$')
                if green_column.empty:
                    continue
                green_totals += green_column.iloc[0]
            load_column = country_columns.filter(regex=f'{LOAD}$')
            if load_column.empty:
                    continue
            load_total = load_column.iloc[0]
            surplus = green_totals - load_total
            surpluses[REGION] = surplus
        max_region = max(surpluses, key=lambda reg: surpluses[reg])
        labels.append(COUNTRY_IDS[max_region])

    # Set a column for sin and cos of time in day, and day in year
    df_filtered_no_nan.index = pd.to_datetime(df_filtered_no_nan.index, format='%Y-%m-%d %H')
    # Calculate sine and cosine values for hour and day
    df_filtered_no_nan['Sin_Hour'] = np.sin(2 * np.pi * df_filtered_no_nan.index.hour / 24)
    df_filtered_no_nan['Cos_Hour'] = np.cos(2 * np.pi * df_filtered_no_nan.index.hour / 24)

    df_filtered_no_nan['Sin_DayOfYear'] = np.sin(2 * np.pi * df_filtered_no_nan.index.dayofyear / 365)
    df_filtered_no_nan['Cos_DayOfYear'] = np.cos(2 * np.pi * df_filtered_no_nan.index.dayofyear / 365)

    df_filtered_no_nan['label']=labels

    df_processed=df_filtered_no_nan

    # Print the resulting DataFrame
    print("\nDataFrame:")
    print(df_processed)
    return df_processed

def save_data(df, output_file):
    # TODO: Save processed data to a CSV file
    df.to_csv(output_file)

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
        default='data/your_train.csv', 
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