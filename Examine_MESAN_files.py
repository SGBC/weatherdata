from METCOMP_utils import *

directory = 'MESAN_Recorded/'
filename = 'MESAN_2020-11-12.txt'

data = load_dict(directory + filename)

# Count number of stations
# Should be 456 if no stations filtered.
print('Number of stations: ' + str(len(data.keys())))



print('\n')
# Count timestamps.
timestamps = {}
for s in data:
    for d in data[s]['frames']:
        timestamps[d] = None
timestamps = list(timestamps)

dt_timestamps = []
for ts in timestamps:
    dt_timestamps.append(ts_to_datetime(ts))

timestamps = sort_by_list(timestamps, dt_timestamps)
print('Number of timestamps found: ' + str(len(timestamps)))


# Check that all stations have the same amount of timestamps.
good_file = True
for s in data:
    tmp_ts = timestamps.copy()
    for d in data[s]['frames']:
        if d in tmp_ts:
            tmp_ts.remove(d)
        else:
            print(d + ' not found. (possible duplicate)')

    if not tmp_ts:
        pass
    else:
        print('station ' + s + ' is missing the following timestamps: ')
        for ts in tmp_ts:
            print(ts)
        good_file = False
        break

if good_file:
    print('All stations have the same timestamps.')
else:
    print('Failed to find all timestamps for all stations.')





print('\n')
# Find all logged parameters.
# Should be 30.
params = {}
for s in data:
    for d in data[s]['frames']:
        for p in data[s]['frames'][d]['parameters']:
            params[p['name'] + '_' + p['levelType']] = None
params = list(params.keys())
print('Number of parameters found: ' + str(len(params)))



# Check that all stations have logged the same parameters (Note this is interpolated data from SMHI.)
good_file = True
for s in data:
    for d in data[s]['frames']:
        tmp_params = params.copy()
        for p in data[s]['frames'][d]['parameters']:
            if p['name'] + '_' + p['levelType'] in tmp_params:
                tmp_params.remove(p['name'] + '_' + p['levelType'])
            else:
                print('Missing param ' + p['name'] + '_' + p['levelType'] + ' for time + ' + d + ' for station ' + s + '.')
                good_file = False
                break
        if not good_file:
            break
    if not good_file:
        break

if good_file:
    print('All frames contain the same parameteres.')
else:
    print('Not all frames contain the same parameters.')



print('\n')
# Find longest name. If utf-8 encoding does not work this should rapidly grow beyond reasonable name strings.
# Should be: Sönnarslöv Öa-Kristinelund
longest_name = ''
for s in data:
    if len(data[s]['name']) > len(longest_name):
        longest_name = data[s]['name']

print('Longest name: ' + longest_name)

