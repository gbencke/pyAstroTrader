import datetime
import json


def create_input_json(date_to_use, parameters_json, config_json):
    input_json = {}
    input = {
        "chart_name": "PETROBRAS",
        "date": date_to_use,
        "latitude": "-22.54",
        "longitude": "-43.14",
        "altitude": "0"
    }

    with open(parameters_json) as fjson:
        parameters = json.load(fjson)
        input_json['parameters'] = parameters

    with open(config_json) as fjson:
        config = json.load(fjson)
        input_json['config'] = config

    input_json['chart'] = input
    return input_json
