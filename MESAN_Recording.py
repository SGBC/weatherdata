from METCOMP_utils import *
import os




def combine_data(old_data, new_data):

    old_stations = list(old_data.keys())

    comb_data = old_data
    for s in new_data:
        # If there exist station in new data which does not exist in old_data, skip it.
        if s not in old_data.keys():
            print('combine_data() >>> station ' + s + ' not in old data. Skipping station')
            continue

        # Combine data
        for ts in new_data[s]['frames']:
            # Do not overwrite old data.
            if ts in old_data[s]['frames']:
                continue
            comb_data[s]['frames'][ts] = new_data[s]['frames'][ts]


        old_stations.remove(s)

    if not old_stations:
        # All stations in old data have got new data.
        pass
    else:
        print('combine_data() >>> The following stations did not receive new data:')
        for e in old_stations:
            print(e)


    return comb_data




def split_data(comb_data):
    # res_data contains a regular data object for each day key.
    # Content of each key in res_data should be written as a
    # separate file.

    # Collect all timestamps.
    timestamps = {}
    for s in comb_data:
        for ts in comb_data[s]['frames']:
            timestamps[ts] = None

    # Get corresponding datetime objects
    timestamps = list(timestamps.keys())
    dt_timestamps = []
    for ts in timestamps:
        tmp_ts = ts.replace("T", " ").strip('Z')
        dt_timestamps.append(datetime.strptime(tmp_ts, '%Y-%m-%d %H:%M:%S'))

    # Sort string timestamps chronologically.
    sorted_ts = sort_by_list(timestamps, dt_timestamps)


    # Init day keys.
    res_data = {}
    for ts in sorted_ts:
        day = ts.split('T')[0]
        res_data[day] = {}

    # Loop over days and init dict structure. Copy station data.
    prev_day = ''
    for ts in sorted_ts:

        day = ts.split('T')[0]
        if day == prev_day:
            continue
        else:
            prev_day = day

        # Add station data for each station and init frames dict.
        res_data[day] = {}
        for s in comb_data:
            res_data[day][s] = {}
            res_data[day][s]['name'] = comb_data[s]['name']
            res_data[day][s]['municId'] = comb_data[s]['municId']
            res_data[day][s]['regionId'] = comb_data[s]['regionId']
            res_data[day][s]['realLong'] = comb_data[s]['realLong']
            res_data[day][s]['realLat'] = comb_data[s]['realLat']
            res_data[day][s]['gridLong'] = comb_data[s]['gridLong']
            res_data[day][s]['gridLat'] = comb_data[s]['gridLat']
            res_data[day][s]['frames'] = {}
            pass

    # Add frames chronologically.
    for ts in sorted_ts:
        day = ts.split('T')[0]
        for s in comb_data:
            res_data[day][s]['frames'][ts] = comb_data[s]['frames'][ts]

    return res_data




LANTMET_URL = 'https://www.ffe.slu.se/lm/json/DownloadJS.cfm'
SMHI_URL = 'https://opendata-download-metanalys.smhi.se/api/category/mesan1g/version/2/geotype/point/lon/{lon}/lat/{lat}/data.json'

# Make a true copy of stations.
stations = get_from_api(LANTMET_URL)

# Collect current data.
data = {}
missing_stations = []
for station in stations:

    # ONLY FOR DEV PURPOSES!!!!
    # REMOVE THIS LATER
    #continue

    real_lat = station['wgs84N']
    real_lon = station['wgs84e']

    # Get latest 24h MESAN data.
    MESAN = get_from_api(SMHI_URL.replace('{lon}', str(real_lon)).replace('{lat}', str(real_lat)))
    if not MESAN:
        # Deal with nonexistent data.
        missing_stations.append(str(station['weatherStationId']))
        continue
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
    print('MESAN_RECORDING: Collected MESAN data for station: ' + str(station['weatherStationId']) + '.')

#print('Size: ' + str(data.__sizeof__()) + ' bytes.')

if not missing_stations:
    print('MESAN_RECORDING: All stations found. (' + str(len(stations)) + ' stations.)')
else:
    print('MESAN_RECORDING: No data found for the following stations:')
    for e in missing_stations:
        print(e)



#save_dict(data, 'MESAN_Test_Dict5.txt')
#quit()




# ========== COMBING AND SPLITTING DATA ==========
# Compare with stored files with similar data and
# add frames which does not exist in stored data.

# This should be data and not loaded from a file
# Only doing this during development.
#data = load_dict('MESAN_Test_Dict4.txt')


directory = 'MESAN_RECORDED/'

# Check dir for saved files
files = []
for r, d, f in os.walk(directory):
    for file in f:
        if '.txt' in file:
            files.append(file)


# If directory empty.
if not files:
    print('MESAN_RECORDING: No previous files exists.')
    res_data = split_data(data)
    for d in res_data:
        print('                 Writing MESAN_' + d + '.txt.')
        save_dict(res_data[d], directory + 'MESAN_' + d + '.txt')


# Find latest file.
# If files overlap, old file will get additional data while a new
# file is written containing contents for the following day.
else:
    print('MESAN_RECORDING: Found previous files.')
    # Third save logic attempt.
    # Check if MESAN_X exists for first date in data.
    # If so, load MESAN_X into old data and combine.

    # Find all dates in data and sort chronologically.
    data_dates = {}  # Dates within fetched data.
    dt_data_dates = []
    for s in data:
        for ts in data[s]['frames']:
            data_dates[ts.split('T')[0]] = None
    data_dates = list(data_dates.keys())
    for d in data_dates:
        dt_data_dates.append(datetime.strptime(d, '%Y-%m-%d'))
    data_dates = sort_by_list(data_dates, dt_data_dates)

    # Check if file containing oldest data exists. If so load it. Otherwise, create two new files.
    merge_file = 'MESAN_' + data_dates[0] + '.txt'
    if merge_file in files:
        print('                 Merging with ' + merge_file)
        old_data = load_dict(directory + merge_file)
        comb_data = combine_data(old_data, data)
        res_data = split_data(comb_data)
        for d in res_data:
            print('                 Writing MESAN_' + d + '.txt.')
            save_dict(res_data[d], directory + 'MESAN_' + d + '.txt')
    # Should enter this if sampling did not occur for 24h.
    else:
        print('                 No file found for merging.')
        res_data = split_data(data)
        for d in res_data:
            print('                 Writing MESAN_' + d + '.txt.')
            save_dict(res_data[d], directory + 'MESAN_' + d + '.txt')




# GOAL
# Filename format: MESAN_YYYY-MM-DD.txt
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