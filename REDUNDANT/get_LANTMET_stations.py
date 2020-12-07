import requests
import json




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
        
        
        
        
# Get dictionary with only the LANTMET stations from the LANTMET API.
# @ returns LANTMET stations and station data in a dictionary.
def get_LANTMET_stations():
    stations_url = 'https://www.ffe.slu.se/lm/json/DownloadJS.cfm?'

    # Get list of all stations.
    stations = get_from_api(stations_url)

    LANTMET_stations = []

    # Put only LANTMET stations in a new dictionary.
    # Constrains: Only stations active between 20150101 and 20200101.
    # OBS!!! What is LantMet Grid??? Remove these?
    # OBS!!! Check with LANTMET how they ID their stations, theory: all ID:s above 20000 is LANTMETS own stations. 
    for station in stations:
        if station['weatherStationId'] > 20000 and station['dataFrom'] <= 20150101 and station['dataTo'] >= 20200101 and not('grib' in station['weatherStationName'].lower()):
            LANTMET_stations.append(station)

    return LANTMET_stations
