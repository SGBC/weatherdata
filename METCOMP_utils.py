import os
import datetime
import requests
import pandas as pd




# Combine data from all CSV files into a dataframe.
# @params stationId: station id as a string.
#         start_date: date object. Includes this date when reading.
#                     example: datetime.date(2020, 9, 1)
#         end_date: date object. Includes this date when reading.
#         folder: determines which folder to get data from (MESAN_CSV or LANTMET_CSV).
#                 folder = True -> MESAN
#                 folder = False -> LANTMET
#                 Can also be a string.
#                 example: folder = 'MESAN' or 'LANTMET'
# @returns comb_df: concatenated dataframe containing all csv data
#                   chronologically. None if a file was not found.
def read_CSV(stationId, folder, start_date, end_date):
    
    # Used if folder is a string to translate to boolean.
    trans_dict = {'MESAN_CSV': True,
                  'MESAN': True,
                  'LANTMET_CSV': False,
                  'LANTMET': False}
    
    # If folder is a string, check if folder is a key in trans_dict.
    if isinstance(folder, str):
        try:
            # folder is assigned a boolean value corresponding to data source.
            folder = trans_dict[folder]
        except KeyError:
            # User provided key not existing in trans_dict.
            print('Key \'' + folder + '\' can not be used to specify data source.')
            return None
    
    if folder:
        station_dir = 'MESAN_CSV/' + stationId + '/'
    else:
        station_dir = 'LANTMET_CSV/' + stationId + '/'
    
    # Check if dir exists.
    if not os.path.isdir(station_dir):
        print('read_CSV() >>> No directory: ' + station_dir)
    
    # Loop over days
    current_date = start_date
    frames = []
    for n in range(0, (end_date - start_date + datetime.timedelta(days=1)).days):
        date_str = current_date.strftime('%Y-%m-%d')
        if folder:
            current_file = 'MESAN_' + date_str + '.csv'
        else:
            current_file = 'LANTMET_' + date_str + '.csv'
        
        # Try to read file, if file not found, return a None object.
        try:
            frames.append(pd.read_csv(station_dir + current_file))
        except IOError as e:
            print('read_CSV() >>> File not found. (' + current_file + ')')
            return None
        
        current_date = current_date + datetime.timedelta(days=1)
    comb_df = pd.concat(frames, ignore_index=True)
    return comb_df




# Get LANTMET parameter data for a selected station over a time interval
# as a pandas dataframe. Missing datapoints is filled to ensure continuity and
# chronological sorting.
# @params id: station id as a string, example: id='149'
#         start_date: date object representing earliest date in selected time interval.
#         end_date: date object representing latest date in selected time interval.
# @returns pandas dataframe with one column for each timestamp and one
#          column per parameter where each row is separated by one hour.
def get_LANTMET(id, start_date, end_date):
    start_str = start_date.strftime('%Y-%m-%d')
    end_str = end_date.strftime('%Y-%m-%d')
    url = 'https://www.ffe.slu.se/lm/json/DownloadJS.cfm?weatherStationID=' + id + '&startDate=' + start_str + '&endDate=' + end_str
    
    # Try accessing API.
    try:
        r = requests.get(url)
    except requests.exceptions.RequestException as e:
        # If accessing API fails
        print('get_LANTMET() >>> Request failed.\n' + str(e.__str__()))
        return None

    # If data is not in JSON format, return.
    try:
        data = r.json()
    except json.JSONDecodeError:
        print('get_LANTMET() >>> Fetched data is not in JSON format.')
        print(r.text)
        return None
    
    # Init dict timestamp keys.
    tmp_dict = {}
    for e in data:
        tmp_dict[e['timeMeasured']] = {'Timestamp': e['timeMeasured'].split('+')[0] + 'Z'}
    
    # Add parameter values.
    params = {}
    for e in data:
        tmp_dict[e['timeMeasured']][e['elementMeasurementTypeId']] = e['value']
        params[e['elementMeasurementTypeId']] = None
    
    # Check if any timestamps are missing, if so fill with None values for each parameter.
    # This also ensures chonologically sorting.
    sorted_data = []
    current_dt = start_date
    for n in range(0, (end_date - start_date + datetime.timedelta(days=1)).days):
        
        for i in range(0, 24):
            # Get string representation of hour.
            hour_str = ''
            if i < 10:
                hour_str = '0' + str(i)
            else:
                hour_str = str(i)
                
            datetime_str = current_dt.strftime('%Y-%m-%d') + 'T' + hour_str + ':00:00'
            # Deal with missing timestamps in fetched data.
            try:
                # Append subdicts to list.
                sorted_data.append(tmp_dict[datetime_str + '+01:00'])
            except KeyError:
                # Timestamp not found in dict. Add one with None values for each param.
                print('Missing data for ' + datetime_str + '.')
                tmp = {}
                tmp['Timestamp'] = datetime_str + 'Z'
                for param in params:
                    tmp[param] = None
                sorted_data.append(tmp)
        current_dt = current_dt + datetime.timedelta(days=1)
        
    res_df = pd.DataFrame(sorted_data)
    return res_df




# Saving a data frame into CSV files (one for each day). 
# @params stationId: station id as a string.
#                    example: '35004'
#         df: data frame as returned from function get_LANTMET. 
#         start_date: date object. OBS: Includes this date when reading.
#                     example: datetime.date(2020, 9, 1)
#         end_date: date object. OBS: Includes this date when reading.
def save_LANTMET(stationId, df, startDate, endDate):
    csv_dir = 'LANTMET_CSV'
    
    # Create directory for LANTMET .csv files.
    if os.path.isdir(csv_dir):
        print(csv_dir + ' exists')
    else:
        print('Creating ' + csv_dir)
        os.mkdir(csv_dir)      
    
    # Create station folder if it not exists.      
    if os.path.isdir(csv_dir + '/'+ stationId + '/'):
        pass
    else:
        print('Creating ' + csv_dir + '/' + stationId + '/' + 'directory.')
        os.mkdir(csv_dir + '/' + stationId + '/')
        
    currentDate = startDate
    for i in range(0,(endDate - startDate + datetime.timedelta(days=1)).days):
        
        # Split out one day from the data frame.
        df_temp = df[df['Timestamp'].str.contains(str(currentDate))]
        
        # Save data into .csv.
        print('Saving ' + 'LANTMET_' + str(currentDate) + '.csv')
        df_temp.to_csv(csv_dir + '/' + stationId + '/' + 'LANTMET_' + str(currentDate) + '.csv', index=False)
        currentDate = currentDate + datetime.timedelta(days=1)
