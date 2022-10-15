from datetime import datetime, timedelta
from collections import defaultdict
from requests import get
import os


def get_api_data(BASE_URL, API_KEY, start_date, end_date):
    """Get NASA API Data for Near Earth Object Asteroids Tracking"""
    API = get(f"{BASE_URL}start_date={start_date}&end_date={end_date}&api_key={API_KEY}")
    if API.status_code == 200:
        return API.json()
    return None


def get_asteroid_info(near_earth_object, dates, element_key, object_type):
    """Get Asteroid Info Structured into a Dictionary"""
    asteroid_info   = defaultdict(list)
    asteroid        = near_earth_object[dates[element_key]][object_type]

    asteroid_close_approach_data    = near_earth_object[dates[element_key]][object_type]['close_approach_data'][0]
    individual_asteroid_data        = get(near_earth_object[dates[element_key]][object_type]['links']['self']).json()
    asteroid_observation_dates      = get_asteroid_observation_dates(individual_asteroid_data)
    asteroid_orbit_class            = get_asteroid_orbit_class(individual_asteroid_data)
    asteroid_orbiting_bodies        = get_asteroid_orbiting_bodies(individual_asteroid_data)

    asteroid_info['id']                     = asteroid['id']
    asteroid_info['name']                   = asteroid['name']
    asteroid_info['diameter_meter']         = asteroid['estimated_diameter']['meters']
    asteroid_info['diameter_feet']          = asteroid['estimated_diameter']['feet']
    asteroid_info['hazardous']              = "Yes" if asteroid['is_potentially_hazardous_asteroid'] is True else "No"
    asteroid_info['close_approach_date']    = asteroid_close_approach_data['close_approach_date_full']
    asteroid_info['current_orbiting_body']  = asteroid_close_approach_data['orbiting_body']
    asteroid_info['velocity_km']            = asteroid_close_approach_data['relative_velocity']['kilometers_per_hour']
    asteroid_info['velocity_miles']         = asteroid_close_approach_data['relative_velocity']['miles_per_hour']
    asteroid_info['orbit_class_type']       = asteroid_orbit_class['orbit_class_type']
    asteroid_info['orbit_type_description'] = asteroid_orbit_class['orbit_class_description']
    asteroid_info['first_observation']      = asteroid_observation_dates['first_observation_date']
    asteroid_info['last_observation']       = asteroid_observation_dates['last_observation_date']
    asteroid_info['orbiting_bodies']        = asteroid_orbiting_bodies

    return asteroid_info


def get_neo_info(near_earth_object, dates):
    """Get a list of informations about each Near Earth Object"""
    neo_info = defaultdict(list)
    for element_key, item in enumerate(dates):
        for object_type in range(len(near_earth_object[item])):
            neo_info[len(neo_info)+1] = get_asteroid_info(near_earth_object,
                                                          dates,
                                                          element_key,
                                                          object_type)

    return neo_info


def get_asteroid_orbiting_bodies(individual_asteroid_data):
    """Get each asteroid orbiting bodies"""
    passing_by_list = set()
    for _, item in enumerate(individual_asteroid_data['close_approach_data']):
        passing_by_list.add(item['orbiting_body'])

    return passing_by_list


def get_asteroid_orbit_class(individual_asteroid_data):
    """Get each asteroid orbiting class"""
    orbit_class = individual_asteroid_data['orbital_data']['orbit_class']

    return orbit_class


def get_asteroid_observation_dates(individual_asteroid_data):
    """Get each asteroid observation dates"""
    observation_dates = individual_asteroid_data['orbital_data']

    return observation_dates


def print_neo_info(neo_info):
    """Print the informations for each asteroid"""
    for asteroid in neo_info:
        print(f"ASTEROID #{asteroid}")
        print(f"\t- ID -> {neo_info[asteroid]['id']}")
        print(f"\t- Name -> {neo_info[asteroid]['name']}")
        print("\t- Observation Dates:")
        print(f"\t\t*First -> {neo_info[asteroid]['first_observation']}")
        print(f"\t\t*Last -> {neo_info[asteroid]['last_observation']}")
        print(f"\t- Potentially Hazardous Asteroid -> {neo_info[asteroid]['hazardous']}")
        print(f"\t- Close Approach Date -> {neo_info[asteroid]['close_approach_date']}")
        print(f"\t- Current Orbiting Body -> {neo_info[asteroid]['current_orbiting_body']}")
        print("\t- Diametre:")
        print(f"\t\t*Min -> {int(neo_info[asteroid]['diameter_meter']['estimated_diameter_min'])}m / {int(neo_info[asteroid]['diameter_feet']['estimated_diameter_min'])}ft")
        print(f"\t\t*Max -> {int(neo_info[asteroid]['diameter_meter']['estimated_diameter_max'])}m / {int(neo_info[asteroid]['diameter_feet']['estimated_diameter_max'])}ft")
        print("\t- Relative Velocity:")
        print(f"\t\t*Km/h -> {neo_info[asteroid]['velocity_km']}")
        print(f"\t\t*Miles/h -> {neo_info[asteroid]['velocity_miles']}")
        print("\t- All Orbiting Bodies -> ", end='')
        print(*neo_info[asteroid]['orbiting_bodies'], sep=', ')
        print("\t- Orbit Class Type:")
        print(f"\t\t*{neo_info[asteroid]['orbit_class_type']} -> {neo_info[asteroid]['orbit_type_description']}")


def fetch_and_print_asteroid_info(BASE_URL, API_KEY, start_date, end_date):
    """Fetch and print each information for each asteroid"""
    data = get_api_data(BASE_URL, API_KEY, start_date, end_date)
    if data:
        num_of_object       = data["element_count"]
        near_earth_object   = data["near_earth_objects"]
        dates               = []

        for i in range(int(start_date[-2:]), int(end_date[-2:])+1):
            dates.append(start_date[:-2]+"%02d" % int(str(i)))

        neo_info = get_neo_info(near_earth_object, dates)
        print_neo_info(neo_info)

        print("\nNumber of Near Earth Object Detected ->", num_of_object)

    else:
        print("NEO Data No Found!")


def clear_console():
    """Clear the console"""
    os.system("cls || clear")


def main():
    """Program Interfact"""
    clear_console()
    print("""
        NASA ~ ASTEROIDS NeoWs
    (Near Earth Object Web Service)
        """)

    timelapse   = input("ENTER TIMELAPSE -> [0 - 7] ")
    timelapse   = int(timelapse) if timelapse.isnumeric() else 0
    end_date    = (datetime.today()).strftime("%Y-%m-%d")
    start_date  = (datetime.today() - timedelta(days=timelapse)).strftime("%Y-%m-%d")
    BASE_URL    = "https://api.nasa.gov/neo/rest/v1/feed?"
    API_KEY     = ""  # --- your key API here --- #

    fetch_and_print_asteroid_info(BASE_URL, API_KEY, start_date, end_date)


if __name__ == "__main__":
    main()
