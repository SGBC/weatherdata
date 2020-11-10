import json
import requests




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
        with open(filename, 'w') as f:
            f.write(json.dumps(data, indent=4, sort_keys=True))
    except OSError:
        print('save_dict() >>> Something went wrong trying to save the file.')




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



# Convert historic json LANTMET data to lst of observations.
# @params data: Dictionary to be saved.
#         params: optional, parameters to be included. Default is all.
# @returns Dictionary containing list of measurements.
def LANTMET_to_lists(data):

    list_data = {'startTime': None, 'endTime': None}
    list_data['startTime'] = data[0]['timeMeasured']
    list_data['endTime'] = data[-1]['timeMeasured']

    # Init keys.
    for e in data:
        list_data[e['elementMeasurementTypeId']] = []

    # Add observations to list.
    for e in data:
        list_data[e['elementMeasurementTypeId']].append(e['value'])

    return list_data



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
