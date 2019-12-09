import dateutil.parser
import swisseph as swe

SEFLG_JPLEPH = 1
SEFLG_SWIEPH = 2
SEFLG_MOSEPH = 4
SEFLG_HELCTR = 8
SEFLG_TRUEPOS = 16
SEFLG_J2000 = 32
SEFLG_NONUT = 64
SEFLG_SPEED3 = 128
SEFLG_SPEED = 256
SEFLG_NOGDEF = 512
SEFLG_NOABERR = 1024
SEFLG_EQUATORIAL = 2048
SEFLG_XYZ = 4096
SEFLG_RADIANS = 8192
SEFLG_BARYCTR = 16384
SEFLG_TOPOCTR = (32 * 1024)
SEFLG_SIDEREAL = (64 * 1024)

NUM_PLANETS = 23


def calculate_house(planet_degree, houses):
    distance = [(i, x - planet_degree, abs(x - planet_degree))
                for i, x in enumerate(houses) if (x - planet_degree) < 0]
    distance_sorted = sorted(distance, key=lambda x: x[2])
    if len(distance_sorted) > 0:
        distance_sorted = distance_sorted[0]
        ret = "{}:{}:{}".format(distance_sorted[0], distance_sorted[2],
                                'sep' if distance_sorted[1] > 0 else 'app')
    else:
        ret = "0:0:0"
    return ret


def calculate_planets_in_houses(chart):
    degrees_planets = chart['planets']['planets_degree_ut']
    houses_planets = [0] * 23
    for i in range(NUM_PLANETS):
        planet_degree = degrees_planets[i]
        houses_planets[i] = calculate_house(planet_degree,
                                            chart['houses']['sh'][0])
    chart['planets']['planets_houses'] = houses_planets
    return chart


def calculate_main_chart(input_data, intermediate, output):
    output['houses'] = {}
    output['houses']['sh'] = {}
    output['houses']['sh'] = swe.houses(
        intermediate['jul_day_UT'], float(input_data['chart']['latitude']),
        float(input_data['chart']['longitude']),
        input_data['config']['house_system'].encode('ascii'))
    output['houses']['houses_degree_ut'] = output['houses']['sh'][0]
    output['houses']['ps'] = swe.nod_aps_ut(
        intermediate['jul_day_UT'], 0, swe.NODBIT_MEAN, intermediate['iflag'])
    output['houses']['pl'] = swe.nod_aps_ut(
        intermediate['jul_day_UT'], 1, swe.NODBIT_MEAN, intermediate['iflag'])

    return output


def calculate_planets(input_data, intermediate, output, config):
    output['planets'] = {}
    output['planets']['planets_sign_name'] = [0] * 23
    output['planets']['planets_degree'] = [0] * 23
    output['planets']['planets_degree_ut'] = [0] * 23
    output['planets']['planets_retrograde'] = [0] * 23

    for i in range(NUM_PLANETS):
        ret_flag = swe.calc_ut(intermediate['jul_day_UT'], i,
                               intermediate['iflag'])
        for x in range(len(config['zodiac'])):
            deg_low = float(x * 30)
            deg_high = float((x + 1) * 30)
            if ret_flag[0] >= deg_low:
                if ret_flag[0] <= deg_high:
                    output['planets']['planets_sign_name'][
                        i] = config['planet_name_short'][i] + ":" + config[
                            'zodiac'][x] + ":" + str(x)
                    output['planets']['planets_degree'][
                        i] = ret_flag[0] - deg_low
                    output['planets']['planets_degree_ut'][i] = ret_flag[0]
                    if ret_flag[3] < 0:
                        output['planets']['planets_retrograde'][i] = True
                    else:
                        output['planets']['planets_retrograde'][i] = False
    return output


def calculate_iflag(input_data):

    config = input_data['config']

    iflag = SEFLG_SWIEPH + SEFLG_SPEED

    if config['postype'] == 'truegeo':
        iflag += SEFLG_TRUEPOS
    if config['postype'] == 'topo':
        iflag += SEFLG_TOPOCTR
    if config['postype'] == 'helio':
        iflag += SEFLG_HELCTR

    if config['zodiactype'] == 'sidereal':
        iflag += SEFLG_SIDEREAL
        swe.set_sid_mode(getattr(swe, 'SIDM_' + config['siderealmode']))

    return iflag


def compute_hour(input_time):
    return input_time.hour + (input_time.minute / 60) + (
        input_time.second / 3600)


def generate_chart(config, input_data):
    input_time = dateutil.parser.parse(input_data["chart"]['date'])

    intermediate = {}
    intermediate['jul_day_UT'] = swe.julday(input_time.year, input_time.month,
                                            input_time.day,
                                            compute_hour(input_time))

    intermediate['geo_loc'] = swe.set_topo(
        float(input_data['chart']['longitude']),
        float(input_data['chart']['latitude']),
        float(input_data['chart']['altitude']))

    intermediate['iflag'] = calculate_iflag(input_data)

    output = {}
    output['input'] = input_data
    output['intermediate'] = intermediate
    output = calculate_planets(input_data, intermediate, output, config)
    output = calculate_main_chart(input_data, intermediate, output)
    output = calculate_planets_in_houses(output)
    return output


def load_config(input_data):
    config = {}
    config['zodiac'] = [
        'aries', 'taurus', 'gemini', 'cancer', 'leo', 'virgo', 'libra',
        'scorpio', 'sagittarius', 'capricorn', 'aquarius', 'pisces'
    ]
    config['planet_name_short'] = [
        'sun', 'moon', 'mercury', 'venus', 'mars', 'jupiter', 'saturn',
        'uranus', 'neptune', 'pluto', 'Node', '?', 'Lilith', '?', 'earth',
        'chiron', 'pholus', 'ceres', 'pallas', 'juno', 'vesta', 'intp. apogee',
        'intp. perigee', 'Asc', 'Mc', 'Dsc', 'Ic', 'DP', 'NP', 'SNode',
        'marriage', 'blacksun', 'vulcanus', 'persephone', 'truelilith'
    ]

    config["postype"] = input_data['config']['postype']
    config["zodiactype"] = input_data['config']['zodiactype']
    config["house_system"] = input_data['config']['house_system']

    return config
