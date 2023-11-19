import argparse
import datetime
import pandas as pd
from dateutil.relativedelta import relativedelta
from utils import perform_get_request, xml_to_load_dataframe, xml_to_gen_data
import threading
import time

basic_info = True
debug_info = True
extra_info = True

def load_api_work(url, params, region, region_data):
    # Use the requests library to get data from the API for the specified time range
    response_content = perform_get_request(url, params)

    # Response content is a string of XML data
    df = xml_to_load_dataframe(response_content)

    # If the region is not in the dictionary, create an empty dataframe for it
    if region not in region_data:
        region_data[region] = pd.DataFrame()

    # Concatenate the current dataframe with the region's dataframe
    region_data[region] = pd.concat([region_data[region], df], ignore_index=True)

    print(f'Got data for {region} :)')

def get_load_data_from_entsoe(regions, periodStart='202302240000', periodEnd='202303240000', output_path='./data', is_threading=True):
    
    #There is a period range limit of 1 year for this API. Processed in 1 year chunks 
    
    # URL of the RESTful API
    url = 'https://web-api.tp.entsoe.eu/api'

    yearStart = int(periodStart[:4])
    yearEnd = int(periodEnd[:4])
    if debug_info:
        print(f'Start year: {yearStart} End year: {yearEnd}')

    dif = yearEnd - yearStart

    # Dictionary to store dataframes for each region
    region_data = {}
    working_threads=[]
    if dif != 0:
        for i in range(dif):
            if i==0:
                year_start_date = periodStart[4:]
            else:
                year_start_date = "01010000"
            #General parameters for the API
            params = {
                'securityToken': '1d9cd4bd-f8aa-476c-8cc1-3442dc91506d',
                'documentType': 'A65',
                'processType': 'A16',
                'outBiddingZone_Domain': 'FILL_IN',   #used for Load data
                'periodStart': str(yearStart + i) + year_start_date,
                'periodEnd': str(yearStart + i + 1) + "01010000"
            }
            if basic_info:
                start_string = datetime.datetime.strptime(params['periodStart'], "%Y%m%d%H%M%S").strftime("%Y-%m-%d %H:%M:%S")
                end_string = datetime.datetime.strptime(params['periodEnd'], "%Y%m%d%H%M%S").strftime("%Y-%m-%d %H:%M:%S")
                print(f"Doing period from: {start_string}, to: {end_string}")

            # Loop through the regions and get data for each region
            for region, area_code in regions.items():
                if basic_info:
                    print(f'Fetching load data for {region}...')
                params['outBiddingZone_Domain'] = area_code

                if not is_threading:
                    load_api_work(url, params, region, region_data)
                elif is_threading:
                    new_thread = threading.Thread(target=load_api_work,args=(url, params, region, region_data))
                    new_thread.start()
                    working_threads.append(new_thread)

    if dif != 0:
        year_start_date = "01010000"
    else:
        year_start_date = periodStart[4:]
    #General parameters for the API
    params = {
        'securityToken': '1d9cd4bd-f8aa-476c-8cc1-3442dc91506d',
        'documentType': 'A65',
        'processType': 'A16',
        'outBiddingZone_Domain': 'FILL_IN',   #used for Load data
        'periodStart': str(yearEnd) + year_start_date,
        'periodEnd': str(yearEnd) + periodEnd[4:]
    }
    if basic_info:
        start_string = datetime.datetime.strptime(params['periodStart'], "%Y%m%d%H%M%S").strftime("%Y-%m-%d %H:%M:%S")
        end_string = datetime.datetime.strptime(params['periodEnd'], "%Y%m%d%H%M%S").strftime("%Y-%m-%d %H:%M:%S")
        print(f"Doing period from: {start_string}, to: {end_string}")

    # Loop through the regions and get data for each region
    for region, area_code in regions.items():
        if basic_info:
            print(f'Fetching load data for {region}...')
        params['outBiddingZone_Domain'] = area_code

        if not is_threading:
            load_api_work(url, params, region, region_data)
        elif is_threading:
            new_thread = threading.Thread(target=load_api_work,args=(url, params, region, region_data))
            new_thread.start()
            working_threads.append(new_thread)

    if is_threading:
        print("Esperadno a que acaben")
        for thread in working_threads:
            thread.join()
        print("Acabaron")
    # Save the dataframes for each region to separate CSV files
    for region, df in region_data.items():
            df.to_csv(f'{output_path}/load_{region}.csv', index=False)

    return




def gen_api_work(url, params, region, region_data, file):
    # Use the requests library to get data from the API for the specified time range
    response_content = perform_get_request(url, params)

    # Response content is a string of XML data
    dfs = xml_to_gen_data(response_content)

    # If the region is not in the dictionary, create an empty directory as its value, that will include the psr_types and corresponding data frames
    if region not in region_data:
        region_data[region] = {}

    # Save each psr_type in region_data[region][psr_type] with corresponding df
    for psr_type in dfs:
        if extra_info:
            print(f'Fetching psr_type: {psr_type} for region: {region}')
            print(f'Fetching psr_type: {psr_type} for region: {region}', file=file)
        
        #If the psr_type is not in the dictionary, create an empty data frame for it
        if psr_type not in region_data[region]:
            region_data[region][psr_type] = pd.DataFrame()
        
        #Cocatenate current data frame of psr_type to existing data frame for psr_type in dict region_data[region]
        region_data[region][psr_type] = pd.concat([region_data[region][psr_type], dfs[psr_type]], ignore_index=True) 
    if basic_info:
        print(f'Got gen data for {region} :)')
        print(f'Got gen data for {region} :)', file=file)


def get_gen_data_from_entsoe(regions, periodStart='202302240000', periodEnd='202303240000', output_path='./data', is_threading=True):
    with open("_output.txt", "w") as file:
    # Set file as empty
        print("GENERATION OUTPUT FOR LAST RUN:", file=file)
    with open("_output.txt", "a") as file: 
        working_threads=[]
        # TODO: There is a period range limit of 1 day for this API. Process in 1 day chunks if needed

        # URL of the RESTful API
        url = 'https://web-api.tp.entsoe.eu/api'

        # Convert start and end periods to datetime objects
        start_date = pd.to_datetime(periodStart, format='%Y%m%d%H%M')
        end_date = pd.to_datetime(periodEnd, format='%Y%m%d%H%M')

        if debug_info:
            print(f'Doing generation from: {start_date.strftime("%Y-%m-%d %H:%M:%S")} to: {end_date.strftime("%Y-%m-%d %H:%M:%S")}.')
            print(f'Doing generation from: {start_date.strftime("%Y-%m-%d %H:%M:%S")} to: {end_date.strftime("%Y-%m-%d %H:%M:%S")}.', file=file)

        # Calculate the number of days between start and end dates
        num_days = (end_date - start_date).days

        if debug_info:
            print(f'Number of days in that interval: {num_days}')
            print(f'Number of days in that interval: {num_days}', file=file)
        # Dictionary to store psr_type dictionaries for each region
        region_data = {}
        
        # General parameters for the API
        params = {
            'securityToken': 'fb81432a-3853-4c30-a105-117c86a433ca',
            'documentType': 'A75',
            'processType': 'A16',
            'outBiddingZone_Domain': 'FILL_IN', # used for Load data
            'in_Domain': 'FILL_IN', # used for Generation data
            'periodStart': periodStart, # in the format YYYYMMDDHHMM
            'periodEnd': periodEnd # in the format YYYYMMDDHHMM
        }
        day_start_period = start_date
        for j in range(num_days):
            #Update days for this query
            day_end_period = day_start_period + datetime.timedelta(days=1)
            params['periodStart'] = day_start_period.strftime("%Y%m%d%H%M")
            params['periodEnd'] = day_end_period.strftime("%Y%m%d%H%M")
            # Loop through the regions and get psr_types dict for each region
            if debug_info and extra_info:
                print(f'-----------------------------------------------------------------------------------------------------------------------------------------')
                print(f'-----------------------------------------------------------------------------------------------------------------------------------------', file=file)
            if debug_info:
                print(f'Day index: {j}/{num_days-1}. From: {day_start_period.strftime("%Y-%m-%d %H:%M:%S")} to : {day_end_period.strftime("%Y-%m-%d %H:%M:%S")}')
                print(f'Day index: {j}/{num_days-1}. From: {day_start_period.strftime("%Y-%m-%d %H:%M:%S")} to : {day_end_period.strftime("%Y-%m-%d %H:%M:%S")}', file=file)
            for region, area_code in regions.items():
                if basic_info:
                    print(f'Fetching gen data for {region}...')
                    print(f'Fetching gen data for {region}...', file=file)
                params['outBiddingZone_Domain'] = area_code
                params['in_Domain'] = area_code
                if not is_threading:
                    gen_api_work(url, params, region, region_data, file)
                elif is_threading:
                    new_thread = threading.Thread(target=gen_api_work,args=(url, params, region, region_data, file))
                    new_thread.start()
                    working_threads.append(new_thread)
            day_start_period = day_end_period #Pass to next day for next iteration  

        for thread in working_threads:
            thread.join()

        #Create final CSV separate files with each info
        for region, region_data_psr_types in region_data.items():
            for psr_type, df in region_data_psr_types.items():
                # #Drop duplicating final dataframe for each psr_type for each region
                # region_data[region][psr_type] = region_data[region][psr_type].drop_duplicates()
                # Save Final DataFrames to separate CSV files for each region and psr_type


                duplicates = df[df.duplicated()]
                # Check if the resulting DataFrame is empty
                if duplicates.empty:
                    print(f"No duplicates found in region: {region}, psr_type: {psr_type}.")
                    print(f"No duplicates found in region: {region}, psr_type: {psr_type}.", file=file)
                else:
                    print("//////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////")
                    print(f"Duplicates found in region: {region}, psr_type: {psr_type}. Rows:")
                    print(duplicates)
                    print("//////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////",file=file)
                    print(f"Duplicates found in region: {region}, psr_type: {psr_type}. Rows:", file=file)
                    print(duplicates, file=file)


                    
                df.to_csv(f'{output_path}/gen_{region}_{psr_type}.csv', index=False)
        
        return

def parse_arguments():
    parser = argparse.ArgumentParser(description='Data ingestion script for Energy Forecasting Hackathon')
    parser.add_argument(
        '--start_time', 
        type=lambda s: datetime.datetime.strptime(s, '%Y-%m-%d'), 
        default=datetime.datetime(2022, 1, 1),
        help='Start time for the data to download, format: YYYY-MM-DD'
    )
    parser.add_argument(
        '--end_time', 
        type=lambda s: datetime.datetime.strptime(s, '%Y-%m-%d'), 
        default=datetime.datetime(2023, 1, 2), 
        help='End time for the data to download, format: YYYY-MM-DD'
    )
    parser.add_argument(
        '--output_path', 
        type=str, 
        default='./data',
        help='Name of the output file'
    )
    return parser.parse_args()

def main(start_time, end_time, output_path):
    
    regions = {
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

    # Transform start_time and end_time to the format required by the API: YYYYMMDDHHMM
    start_time = start_time.strftime('%Y%m%d%H%M')
    end_time = end_time.strftime('%Y%m%d%H%M')

    t1 = time.time()
    # Get Load data from ENTSO-E
    get_load_data_from_entsoe(regions, start_time, end_time, output_path)
    t2 = time.time()
    print(f"load took with threading: {t2-t1}s.")

    # Get Generation data from ENTSO-E
    t1 = time.time()
    get_gen_data_from_entsoe(regions, start_time, end_time, output_path)
    t2 = time.time()
    print(f"load took with threading: {t2-t1}s.")

if __name__ == "__main__":
    args = parse_arguments()
    main(args.start_time, args.end_time, args.output_path)