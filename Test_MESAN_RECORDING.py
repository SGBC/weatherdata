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



# CHECK THAT NEW TIMESTAMPS EXIST
dir = 'MESAN_RECORDED/'

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




