import os
import datetime
import requests
import pandas as pd




# Combine data from all CSV files into a dataframe.
# @params stationId: station id as a string.
#         start_date: date object. Includes this date when reading.
#                     example: datetime.date(2020, 9, 1)
#         end_date: date object. Includes this date when reading.
#         type: determines whether to load MESAN (SMHI) or LANTMET data.
#               type = True -> MESAN
#               type = False -> LANTMET
# @returns comb_df: concatenated dataframe containing all csv data
#                   chronologically. None if a file was not found.
def read_CSV(stationId, type, start_date, end_date):
    
    if type:
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
        if type:
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
