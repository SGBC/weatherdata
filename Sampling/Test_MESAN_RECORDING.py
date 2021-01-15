from METCOMP_utils import *
import os


# Find all unique timestamps in recorded MESAN data.
# @params data: data to be checked.
# @returns list of timestamps.
def get_timestamps(data):
    timestamps = {}
    dt_timestamps = []
    for s in data:
        for ts in data[s]['frames']:
            timestamps[ts] = None

    timestamps = list(timestamps.keys())

    print(timestamps)



# Checks formatted data if all hours have been logged for all stations within data.
# @params data: Data to be checked.
# @returns bool: True if all hours are logged for each stations. Otherwise false.
def check_if_complete(data):
    for s in data:

        # Create list of timestamps as reference.
        timestamps_ref = []
        for i in range(0, 23):
            hour_str = ''
            if i < 10:
                hour_str = '0' + str(i)
            else:
                hour_str = str(i)
            tmp_str = '2020-11-11T' + hour_str + ':00:00Z'
            timestamps_ref.append(tmp_str)

        # Find all timestamps.
        timestamps = list(data[s]['frames'].keys())

        print(timestamps_ref)
        print(timestamps)
        quit()


        # Check if all timestamps exist.



directory = 'MESAN_RECORDED/'
filename= 'MESAN_2020-11-10.txt'
data = load_dict(directory + filename)

print(data['149']['frames'].keys())

if check_if_complete(data):
    print('File is complete.')
else:
    print('File is not complete.')

# CHECK THAT NEW TIMESTAMPS EXIST
directory = 'MESAN_RECORDED/'

files = []
for r, d, f in os.walk(dir):
    for file in f:
        if '.txt' in file:
            files.append(file)

days = []
dt_days = []
for file in files:
    day = file.split('_')[1].split('.')[0]
    days.append(day)

    dt_days.append(datetime.strptime(day, '%Y-%m-%d'))

days = sort_by_list(days, dt_days)
latest_file = 'MESAN_' + days[-1] + '.txt'

data = load_dict(dir + latest_file)

timestamps = get_timestamps(data)


# CHECK THAT OLD FILES ARE UNCHANGED


