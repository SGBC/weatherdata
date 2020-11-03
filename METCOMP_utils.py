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



