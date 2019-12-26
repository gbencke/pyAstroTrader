import datetime
import json
import pprint

from pyastrotrader import calculate_chart
from pyastrotrader import calculate_aspects
from pyastrotrader import calculate_transits
from pyastrotrader.constants import *


def create_input_json(date_to_use):
    input_json = {}
    input = {
        "chart_name": "PETROBRAS",
        "date": date_to_use,
        "latitude": "-22.54",
        "longitude": "-43.14",
        "altitude": "0"
    }

    parameters_json = "../pyastrotrader/test/default_parameters.json"
    with open(parameters_json) as fjson:
        parameters = json.load(fjson)
        input_json['parameters'] = parameters

    config_json = "../pyastrotrader/test/default_config.json"
    with open(config_json) as fjson:
        config = json.load(fjson)
        input_json['config'] = config

    input_json['chart'] = input
    return input_json


if __name__ == "__main__":
    main_chart_input_json = create_input_json('1953-10-03T19:05:00-03:00')
    petr4_chart = calculate_chart(main_chart_input_json)

    # today_date = datetime.datetime.now().strftime("%Y-%m-%dT10:00:00-03:00")
    today_date = "2019-12-23T05:00:00-03:00"
    today_chart_input_json = create_input_json(today_date)
    today_chart = calculate_chart(today_chart_input_json)

    planets_to_aspect = [SUN, MOON, JUPITER, SATURN]
    aspects_to_calculate = [CONJUNCTION, SEMISQUARE, SEXTILE, SQUARE, TRINE, OPPOSITION]

    pp = pprint.PrettyPrinter(depth=6)

    detected_aspects = calculate_aspects(petr4_chart, planets_to_aspect, aspects_to_calculate, 4)
    # pp.pprint(detected_aspects)

    detected_transits = calculate_transits(petr4_chart, today_chart, planets_to_aspect, aspects_to_calculate, 4)
    pp.pprint(detected_transits)
