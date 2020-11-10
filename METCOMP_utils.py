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
