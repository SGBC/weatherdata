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
            frames.append(pd.read_csv(station_dir + current_file, sep=';'))
        except IOError as e:
            print('read_CSV() >>> File not found. (' + current_file + ')')
            return None
        
        current_date = current_date + datetime.timedelta(days=1)
    comb_df = pd.concat(frames, ignore_index=True)
    return comb_df




# Get LANTMET parameter data for a selected station over a time interval
# as a pandas dataframe. Missing datapoints is filled to ensure continuity and
# chronological sorting.
# UPDATED: Since LANTMETS api seems to not allow an extraction for a large time interval, the extraction
# is made in chunks of chunk_size(default=200) days.
# @params id: station id as a string, example: id='149'
#         start_date: date object representing earliest date in selected time interval.
#         end_date: date object representing latest date in selected time interval.
# @returns pandas dataframe with one column for each timestamp and one
#          column per parameter where each row is separated by one hour.
def get_LANTMET(id, start_date, end_date):
    #start_str = start_date.strftime('%Y-%m-%d')
    #end_str = end_date.strftime('%Y-%m-%d')
    #url = 'https://www.ffe.slu.se/lm/json/DownloadJS.cfm?weatherStationID=' + id + '&startDate=' + start_str + '&endDate=' + end_str
    
    chunk_size = 200
    
    total_days = (end_date - start_date + datetime.timedelta(days=1)).days
    n200 = total_days // chunk_size
    remainder_days = total_days % chunk_size
    #print(total_days)
    #print(n200)
    #print(remainder_days)
    
    # List of dicts. Will be converted to DataFrame.
    dict_list = []
    
    # Loop over number of 200d intervals in total interval.
    current_date = start_date
    for i200 in range(0, n200):
        
        tmp_start = current_date.strftime('%Y-%m-%d')
        tmp_end = (current_date + datetime.timedelta(days=chunk_size)).strftime('%Y-%m-%d')
        url = 'https://www.ffe.slu.se/lm/json/DownloadJS.cfm?weatherStationID=' + id + '&startDate=' + tmp_start + '&endDate=' + tmp_end
        #print(tmp_start)
        #print(tmp_end)
        #print(url)
        #continue
        
        #print(current_date)
        
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
        
        # Reformat data to bring search time to O(1).
        tmp_dict = {}
        for e in data:
            tmp_dict[e['timeMeasured']] = {'Timestamp': e['timeMeasured'].split('+')[0] + 'Z'}
        for e in data:
            tmp_dict[e['timeMeasured']][e['elementMeasurementTypeId']] = e['value']
        
        for d in range(0, chunk_size):#+1):
            
            for h in range(0, 24):
                hour_str = ''
                if h < 10:
                    hour_str = '0' + str(h)
                else:
                    hour_str = str(h)
                    
                datetime_str = current_date.strftime('%Y-%m-%d') + 'T' + hour_str + ':00:00'
                
                # Append dict corresponding to current datetime. If not found, warn user.
                try:
                    dict_list.append(tmp_dict[datetime_str + '+01:00'])
                except KeyError:
                    print('get_LANTMET() >>> Missing data for ' + datetime_str + '.')
                    tmp = {'Timestamp': datetime_str + 'Z'}
                    dict_list.append(tmp)
            
            current_date = current_date + datetime.timedelta(days=1)
        #current_date = current_date + datetime.timedelta(days=1)
        #print(current_date)
    
    
    
    
    # Fetch remaining days.
    tmp_start = current_date.strftime('%Y-%m-%d')
    tmp_end = (current_date + datetime.timedelta(days=remainder_days-1)).strftime('%Y-%m-%d')
    url = 'https://www.ffe.slu.se/lm/json/DownloadJS.cfm?weatherStationID=' + id + '&startDate=' + tmp_start + '&endDate=' + tmp_end
    
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
    
    # Reformat data to bring search time to O(1).
    tmp_dict = {}
    for e in data:
        tmp_dict[e['timeMeasured']] = {'Timestamp': e['timeMeasured'].split('+')[0] + 'Z'}
    for e in data:
        tmp_dict[e['timeMeasured']][e['elementMeasurementTypeId']] = e['value']
    
    #print(tmp_start)
    #print(tmp_end)
    #print(url) 
    for d in range(0, remainder_days):
        for h in range(0, 24):
            hour_str = ''
            if h < 10:
                hour_str = '0' + str(h)
            else:
                hour_str = str(h)
                    
            datetime_str = current_date.strftime('%Y-%m-%d') + 'T' + hour_str + ':00:00'
                
            # Append dict corresponding to current datetime. If not found, warn user.
            try:
                dict_list.append(tmp_dict[datetime_str + '+01:00'])
            except KeyError:
                print('get_LANTMET() >>> Missing data for ' + datetime_str + '.')
                tmp = {'Timestamp': datetime_str + 'Z'}
                dict_list.append(tmp)
            
        current_date = current_date + datetime.timedelta(days=1)
    
    return(pd.DataFrame(dict_list))




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
        
        
        

# Splitting dataframe into bins corresponding to months 
# @params df: dataframe as returned from read_CSV.
# @returns dictionary with keys for each month containing all rows of the corresponding month.
# {1: df_january, 2: df_february, ..., 12: df_december}
def divide_months(df):
    months = {}
    for month in range(1, 13):
        
        # Get hour string as two character string.
        month_str = ''
        if month < 10:
            month_str = '0' + str(month)
        else:
            month_str = str(month)
        months[month] = df[df['Timestamp'].str.contains('-' + month_str + '-')]
        
    return months




# Splitting dataframe into bins corresponding to weeks 
# @params df: dataframe as returned from read_CSV.
# @returns dictionary with keys for each week containing all rows of the corresponding week.
# {1: df_week1, 2: df_week2, ..., 52: df_week52}
def divide_weeks(df):
    
    # Initialize variables.
    week = df.iloc[0]['Timestamp'].split('T')[0]
    week = datetime.datetime.strptime(week, '%Y-%m-%d').isocalendar()[1]
    prev_week = week
    weeks = {}
    start_index = 0
    end_index = 0
    
    # Loop over every row.
    for index, df_row in df.iterrows():
        
        # Find week number.
        current_dt = df_row['Timestamp'].split('T')[0]
        current_dt = datetime.datetime.strptime(current_dt, '%Y-%m-%d')
        week = current_dt.isocalendar()[1]
        
        # If change in current week, slice all rows appertaining to previous week and try to concatenate with previous dataframes.
        if not week == prev_week:       
            end_index = index
            try:
                # If previous data exists, concatenate dataframes
                weeks[prev_week] = pd.concat([weeks[prev_week], df.iloc[start_index:end_index]])
            except KeyError:
                # If no previous data exists, initialize key and concatenate to None object.
                weeks[prev_week] = None
                weeks[prev_week] = pd.concat([weeks[prev_week], df.iloc[start_index:end_index]])
            start_index = end_index
        
        prev_week = week
    
    return weeks




# Splitting dataframe into bins corresponding to hours 
# @params df: dataframe as returned from read_CSV.
# @returns dictionary with keys for each hour containing all rows of the corresponding hour.
# {0: hour0, 1: df_hour1, ..., 23: df_hour23}
def divide_hours(df):
    
    hours = {}
    
    for hour in range(0, 24):
        
        # Get hour string as two character string.
        hour_str = ''
        if hour < 10:
            hour_str = '0' + str(hour)
        else:
            hour_str = str(hour)
        hours[hour] = df[df['Timestamp'].str.contains('T' + hour_str)]
        
    return hours
