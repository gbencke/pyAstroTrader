from ..constants import *


def already_added(found_aspects, c_planet, n_planet, c_aspect):
    search = [x for x in found_aspects if
              (x['c_aspect'] == c_aspect and x['c_planet'] == c_planet and x['n_planet'] == n_planet) or (
                      x['c_aspect'] == c_aspect and x['c_planet'] == n_planet and x['n_planet'] == c_planet)]
    return len(search) > 0


def get_degrees(chart, planetA, planetB):
    c_planet_degreeA = chart['planets']['planets_degree_ut'][planetA]
    c_planet_degreeB = chart['planets']['planets_degree_ut'][planetB]
    return c_planet_degreeA - c_planet_degreeB

def calculate_aspects(chart, planets, transits, tolerance):
    found_aspects = []

    for c_aspect in transits:
        c_aspect_angle = ASPECT_DEGREE[c_aspect]
        for c_planet in planets:
            c_planet_degree = chart['planets']['planets_degree_ut'][c_planet]
            for n_planet in planets:
                if c_planet == n_planet:
                    continue
                n_planet_degree = chart['planets']['planets_degree_ut'][n_planet]
                current_separation = abs(n_planet_degree - c_planet_degree)
                current_tolerance = abs(current_separation - c_aspect_angle)
                if abs(current_tolerance) < tolerance:
                    if not already_added(found_aspects, c_planet, n_planet, c_aspect):
                        found_aspects.append({
                            "c_aspect_name": ASPECT_NAME[c_aspect],
                            "n_planet_name": PLANETS[n_planet],
                            "c_planet_name": PLANETS[c_planet],
                            "c_planet": c_planet,
                            "c_planet_degree": c_planet_degree,
                            "n_planet": n_planet,
                            "n_planet_degree": n_planet_degree,
                            "c_aspect": c_aspect,
                            "c_aspect_angle": c_aspect_angle,
                            "c_aspect_separation": current_separation})

    return found_aspects


def calculate_transits(radix_chart, transiting_chart, planets, transits, tolerance):
    found_transits = []

    for c_aspect in transits:
        c_aspect_angle = ASPECT_DEGREE[c_aspect]
        for c_planet in planets:
            c_planet_degree = radix_chart['planets']['planets_degree_ut'][c_planet]
            for n_planet in planets:
                n_planet_degree = transiting_chart['planets']['planets_degree_ut'][n_planet]
                current_separation = abs(n_planet_degree - c_planet_degree)
                current_tolerance = abs(current_separation - c_aspect_angle)
                if abs(current_tolerance) < tolerance:
                    if not already_added(found_transits, c_planet, n_planet, c_aspect):
                        found_transits.append({
                            "c_aspect_name": ASPECT_NAME[c_aspect],
                            "n_planet_name": PLANETS[n_planet],
                            "c_planet_name": PLANETS[c_planet],
                            "c_planet": c_planet,
                            "c_planet_degree": c_planet_degree,
                            "n_planet": n_planet,
                            "n_planet_degree": n_planet_degree,
                            "c_aspect": c_aspect,
                            "c_aspect_angle": c_aspect_angle,
                            "c_aspect_separation": current_separation})

    return found_transits
