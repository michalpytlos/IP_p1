"""Extract data on near-Earth objects and close approaches from CSV and JSON files.

The `load_neos` function extracts NEO data from a CSV file, formatted as
described in the project instructions, into a collection of `NearEarthObject`s.

The `load_approaches` function extracts close approach data from a JSON file,
formatted as described in the project instructions, into a collection of
`CloseApproach` objects.

The main module calls these functions with the arguments provided at the command
line, and uses the resulting collections to build an `NEODatabase`.

You'll edit this file in Task 2.
"""
import csv
import json

from models import NearEarthObject, CloseApproach


def load_neos(neo_csv_path):
    """Read near-Earth object information from a CSV file.

    :param neo_csv_path: A path to a CSV file containing data about near-Earth objects.
    :return: A collection of `NearEarthObject`s.
    """
    neos = []
    with open(neo_csv_path) as f:
        reader = csv.DictReader(f)
        for row in reader:
            neo = NearEarthObject(row['pdes'],
                                  row['name'],
                                  row['diameter'],
                                  row['pha'])
            neos.append(neo)
    return neos


def load_approaches(cad_json_path):
    """Read close approach data from a JSON file.

    :param neo_csv_path: A path to a JSON file containing data about close approaches.
    :return: A collection of `CloseApproach`es.
    """
    cas = []
    with open(cad_json_path) as f:
        file_data = json.load(f)
        labels = file_data['fields']
        designation_index = labels.index('des')
        time_index = labels.index('cd')
        distance_index = labels.index('dist')
        velocity_index = labels.index('v_rel')
        for ca_data in file_data['data']:
            cs = CloseApproach(ca_data[designation_index],
                               ca_data[time_index],
                               ca_data[distance_index],
                               ca_data[velocity_index])
            cas.append(cs)
    return cas
