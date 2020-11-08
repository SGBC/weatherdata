from METCOMP_utils import *

LANTMET_URL = 'https://www.ffe.slu.se/lm/json/DownloadJS.cfm'
SMHI_URL = 'https://opendata-download-metanalys.smhi.se/api/category/mesan1g/version/2/geotype/point/lon/{lon}/lat/{lat}/data.json'

stations = get_from_api(LANTMET_URL)


# Collect current data.
data = {}
for station in stations:

    real_lat = station['wgs84N']
    real_lon = station['wgs84e']

    # Get latest 24h MESAN data.
    MESAN = get_from_api(SMHI_URL.replace('{lon}', str(real_lon)).replace('{lat}', str(real_lat)))
    if not MESAN:
        # Deal with nonexistent data.
        pass
    elif True:
        # Data might be incomplete?
        pass

    # Collect grid point coordinates of interpolated data. (Not necessarily same as real coordinates)
    # Assumption: Grid coordinates are static, i.e. does not change over time. (Suggest confirming with SMHI)
    grid_lon = MESAN['geometry']['coordinates'][0][0]
    grid_lat = MESAN['geometry']['coordinates'][0][1]

    data_station = data[str(station['weatherStationId'])] = {}
    data_station['name'] = station['weatherStationName']
    data_station['municId'] = station['MunicID']
    data_station['regionId'] = station['RegionID']
    data_station['realLong'] = real_lon
    data_station['realLat'] = real_lat
    data_station['gridLong'] = grid_lon
    data_station['gridLat'] = grid_lat

    data_station['frames'] = {}

    # Loop over every hour in timeseries.
    for e in MESAN['timeSeries']:
        data_station['frames'][e['validTime']] = {}
        data_station['frames'][e['validTime']]['parameters'] = e['parameters']

    #print_dict(data)
    #print(data['149']['frames'].keys())
    print('Collected MESAN for station: ' + str(station['weatherStationId']) + '.')

print('Size: ' + str(data.__sizeof__()) + ' bytes.')
quit()


# Compare with stored files with similar data and
# add frames which does not exist in stored data.
# TODO


# GOAL
# One file for each day containing the following JSON data.
# Each file should contain frames from T00:00:00Z to T23:00:00Z
#
# data[stationID][validTime][parameter]
#{
#    "ID1" : {
#        "realLat" : lat
#        "realLong" : long
#        "gridLat" : gridlat
#        "gridlong" : gridlong
#        // kanske några extra stationsspecifika egenskaper som namn, municID osv...
#        "frames" : {
#            "2020-11-08T00:00:00Z" : {
#                "parameters" : [
#                    ...
#                ]
#            },
#            "2020-11-08T01:00:00Z" : {
#                ...
#            },
#            ...
#            "2020-11-08T23:00:00Z" : {
#                ...
#            }
#        }
#    },
#    "ID2" : {
#        ...
#    },
#    ...
#}