import pprint

from pyastrotrader import calculate_chart
from pyastrotrader import calculate_aspects
from pyastrotrader import calculate_transits
from pyastrotrader.utils import create_input_json
from pyastrotrader.constants import *

if __name__ == "__main__":
    parameters_json = "../pyastrotrader/test/default_parameters.json"
    config_json = "../pyastrotrader/test/default_config.json"
    main_chart_input_json = create_input_json('1953-10-03T19:05:00-03:00', parameters_json, config_json)
    petr4_chart = calculate_chart(main_chart_input_json)

    today_date = "2019-12-23T05:00:00-03:00"
    today_chart_input_json = create_input_json(today_date, parameters_json, config_json)
    today_chart = calculate_chart(today_chart_input_json)

    planets_to_aspect = [SUN, MOON, JUPITER, SATURN]
    aspects_to_calculate = [CONJUNCTION, SEMISQUARE, SEXTILE, SQUARE, TRINE, OPPOSITION]

    pp = pprint.PrettyPrinter(depth=6)

    detected_aspects = calculate_aspects(petr4_chart, planets_to_aspect, aspects_to_calculate, 4)
    # pp.pprint(detected_aspects)

    detected_transits = calculate_transits(petr4_chart, today_chart, planets_to_aspect, aspects_to_calculate, 4)
    pp.pprint(detected_transits)
