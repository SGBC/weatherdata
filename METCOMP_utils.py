import json
import requests
from datetime import datetime



# Pretty prints a dictionary.
# @params data: Dictionary to be pretty printed.
# @returns None.
def print_dict(data):
    print(json.dumps(data, indent=4, sort_keys=False))




# Saves a dictionary to a file
# @params data: Dictionary to be saved.
#         filename: Name of saved file.
# @returns None.
def save_dict(data, filename):
    try:
        with open(filename, 'w', encoding='utf8') as f:
            f.write(json.dumps(data, indent=4, sort_keys=False, ensure_ascii=False))
    except OSError:
        print('save_dict() >>> Something went wrong trying to save the file.')




# Load JSON data from file
# @params filename: Name of file containing JSON data.
# @returns data: Dict with JSON data.
def load_dict(filename):
    with open(filename, 'r') as f:
        data = json.load(f)
    return data




# Convert string timestamp to datetime object.
# @params timestamp: string timestamp (YYYY-MM-DDTHH:MM:SSZ).
# @returns dt_obj: datetime object of timestamp.
def ts_to_datetime(timestamp):
    timestamp = timestamp.strip('Z')
    dt = timestamp.split('T')

    ymd = dt[0].split('-')
    ymd = [int(x) for x in ymd]

    hms = dt[1].split(':')
    hms = [int(x) for x in hms]

    dt_obj = datetime(ymd[0], ymd[1], ymd[2], hms[0], hms[1], hms[2])
    return dt_obj




# Sorts list X by list X. For example if X contains strings of ints and Y actual ints,
# X can be sorted by performing the same operations as when sorting Y.
# @params: X, Y: lists of elements. Y must contain comparable objects.
# @returns: X sorted by Y.
def sort_by_list(X, Y):
    return [x for _, x in sorted(zip(Y, X))]




# Tries to access an url for json object data.
# @params data: Dictionary to be saved.
# @returns Dictionary of json object.
def get_from_api(url):

    try:
        # Try accessing API.
        r = requests.get(url)
    except requests.exceptions.RequestException as e:
        # If accessing API fails
        print('get_from_api() >>> Request failed.\n' + str(e.__str__()))
        return None

    # This is necessary if returned data is not JSON format.
    try:
        return r.json()
    except json.JSONDecodeError:
        print('get_from_api() >>> Data is not in JSON format.')
        print(r.text)
        return None



# Convert historic json LANTMET data to list of observations.
# @params data: Dictionary to be saved.
#         params: optional, parameters to be included. Default is all.
# @returns Dictionary containing list of measurements.
def LANTMET_to_lists(data):

    list_data = {'startTime': None, 'endTime': None}
    list_data['startTime'] = data[0]['timeMeasured']
    list_data['endTime'] = data[-1]['timeMeasured']

    # Init keys with lists.
    for e in data:
        list_data[e['elementMeasurementTypeId']] = []

    # Add observations to list.
    for e in data:
        list_data[e['elementMeasurementTypeId']].append(e['value'])

    return list_data




# Trial function to replace original. Verify points are spaced by 1h.
def LANTMET_to_lists2(data):

    list_data = {'startTime': None, 'endTime': None}
    list_data['startTime'] = data[0]['timeMeasured']
    list_data['endTime'] = data[-1]['timeMeasured']

    try:
        list_data['startTime'] = data[0]['timeMeasured']
    except KeyError:
        pass

    # Init lists with number elements = number of hours between startTime and endTime
    # [hour0, hour1, hour2, hour3, hour4]
    # If no measurement for hourX,

    for e in list_data:
        pass

        # shift to next elements by newTime - oldTime hours



# Convert historic (last 24 hours) json MESAN data to lists.
# Do not save tmin and tmax that are given once a day.
# @params data: Dictionary to be saved.
#         params: optional, parameters to be included. Default is all.
# @returns Dictionary containing list of measurements.
def MESAN_to_lists(data):

    list_data = {'startTime': None, 'endTime': None}
    list_data['startTime'] = data['timeSeries'][-1]['validTime']
    list_data['endTime'] = data['timeSeries'][0]['validTime']

    # Init keys.
    for e in data['timeSeries'][0]['parameters']:
        list_data[e['name']] = []

    # Add observations to list in reverse order (oldest to newest).
    for i in range(len(data['timeSeries'])-1, 0, -1):
        for e in data['timeSeries'][i]['parameters']:
            if e['name'] in list_data:
                list_data[e['name']].append(e['values'][0])

    return list_data

# Get historic json LANTMET data for ONE STATION from API between start date and end date.
# @params stationID: weatherStationID in LANTMET API
#         start_date: as a string, ex. '2020-01-02'  
#         end_date: as a string.
# @returns dictionary with parameters for the specified station between given dates
def get_LANTMET_data_station(stationId,startDate,endDate,startTime=None,endTime=None): 
    
    url_lantmet = 'https://www.ffe.slu.se/lm/json/DownloadJS.cfm?weatherStationID='+stationId+'&startDate='+startDate+'&endDate='+endDate+'&startTime='+startTime+'&endTime='+endTime
    data_lantmet = get_from_api(url_lantmet) 
    
    return data_lantmet

# Create a new dictionary for historic json LANTMET for ONE STATION between start date/time and end date/time.
# OBS. The format of the dictionary is the same as for sampled MESAN data.
# @params station: station data as given from the API (returned form get_LANTMET_data_station)
#         startDate: as a string, ex. '2020-01-02'. 
#         endDate: as a string.
#         startTime: as a string, ex. '08'
#         endTime: as a string.
# @returns dictionary with parameters for the specified station between given dates (on the same form as sampled MESAN data).
def LANTMET_dict(station,startDate,endDate,startTime,endTime):
    # Initializes station dictionary.
    station_id = str(station['weatherStationId'])
    new_data[station_id] = {}

    # Add keys and station data.
    new_data[station_id]['name'] = station['weatherStationName']
    new_data[station_id]['municId'] = station['MunicID']
    new_data[station_id]['regionId'] = station['RegionID']
    new_data[station_id]['realLong'] = station['wgs84e']
    new_data[station_id]['realLat'] = station['wgs84N']

    # Initializes frames dictionary.
    new_data[station_id]['frames'] = {}

    # Get parameter data.
    param_data = get_LANTMET_data_station(station_id,startDate,endDate,startTime,endTime)

    # Collect all timestamps and sort from earliest to latest.
    timestamps = {}
    for e in param_data:
        # Convert time format from '+01:00' to 'Z'.
        timestamps[station['timeMeasured'].split('+')[0] + 'Z'] = None

    timestamps = list(timestamps.keys())

    # Need list of datetime representations of timestamps in order to compare chronologically and sort.
    dt_timestamps = []
    for ts in timestamps:
        dt_timestamps.append(ts_to_datetime(ts))

    # Sort string timestamps based on how dt_timestamps would be sorted.
    timestamps = sort_by_list(timestamps, dt_timestamps)

    # Now we have sorted string timestamps. Loop over these and find corresponding measurements.
    for ts in timestamps:

        new_data[station_id]['frames'][ts] = {'parameters': []}

        for e in param_data:

            # Skip observations not made on this timestamp.
            e_timestamp = e['timeMeasured'].split('+')[0] + 'Z'
            if e_timestamp != ts:
                continue

            # Make temporary dictionary. This will become the elements under 'parameters'.
            tmp_dict = {}
            tmp_dict['name'] = e['elementMeasurementTypeId']
            tmp_dict['logIntervalId'] = e['logIntervalId']
            tmp_dict['values'] = [e['value']]
            new_data[station_id]['frames'][ts]['parameters'].append(tmp_dict)
            
    return new_data[station_id]


# Get historic json LANTMET data for ALL stations from API between start date/time and end date/time.
# @params startDate: as a string, ex. '2020-01-02'.
#         endDate: as a string.
#         startTime: as a string, ex. '08'
#         endTime: as a string.
# @returns dictionary with data for ALL stations for specified dates.
def get_LANTMET_data(startDate,endDate,startTime,endTime):
    stations_url = 'https://www.ffe.slu.se/lm/json/DownloadJS.cfm?'

    # Get list of all stations.
    stations = get_from_api(stations_url)

    new_data = {}
    for station in stations:
        new_data[station['weatherStationId']] = LANTMET_dict(station,startDate,endDate,startTime,endTime)
        print_dict(new_data)
    return new_data


