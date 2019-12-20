import os
import sys
import swisseph as swe

from pyastrotrader.calculate import load_config, generate_chart


def show_usage():
    pass


def check_key_exists(json_dict, key, key2=None):
    if key not in json_dict:
        return None
    else:
        if key2 is None:
            return json_dict[key]
        else:
            if key2 in json_dict[key]:
                return json_dict[key][key2]
            else:
                return json_dict


def check_json(json_parsed):
    for key in [('config', 'postype'), ('config', 'zodiactype'),
                ('config', 'house_system'), ('chart', 'longitude'),
                ('chart', 'date'), ('chart', 'latitude'), ('chart',
                                                           'altitude')]:
        if check_key_exists(json_parsed, key[0], key[1]) is None:
            raise ValueError("Key:{}/{} is expected in json".format(
                key[0], key[1]))


def check_input(input_json):
    try:
        if 'SWISSEPH_PATH' in os.environ:
            ephe_path = os.environ['SWISSEPH_PATH']
        else:
            raise ValueError("SWISSEPH_PATH must be set....")

        if os.path.isdir(ephe_path):
            swe.set_ephe_path(ephe_path)
        else:
            raise ValueError("Error, swiss ephemeris was not found")

        check_json(input_json)

        return input_json
    except Exception as e:
        raise ValueError(str(e))


def calculate_chart(input_json):
    input_data = check_input(input_json)
    config = load_config(input_data)
    output = generate_chart(config, input_data)
    return output


__all__ = ['calculate_chart']
