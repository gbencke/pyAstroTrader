import json
from pyastrotrader import calculate_chart

if __name__ == "__main__":
    chart_json = {}
    input = {
        "chart_name": "Guilherme Bencke Natal Chart",
        "date": "1976-12-07T12:30:00-03:00",
        "latitude": "-30.03",
        "longitude": "-51.2204",
        "altitude": "0"
    }

    parameters_json = "../pyastrotrader/test/default_parameters.json"
    with open(parameters_json) as fjson:
        parameters = json.load(fjson)
        chart_json['parameters'] = parameters

    config_json = "../pyastrotrader/test/default_config.json"
    with open(config_json) as fjson:
        config = json.load(fjson)
        chart_json['config'] = config

    chart_json['chart'] = input

    print(json.dumps(chart_json, indent=4))
    calculated_chart = calculate_chart(chart_json)
    print(json.dumps(calculated_chart, indent=4))
