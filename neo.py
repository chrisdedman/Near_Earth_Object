from datetime import datetime, timedelta
from collections import defaultdict
from requests import get
from datetime import datetime
import os


def get_data(BASE_URL, API_KEY, start_date, end_date):
    """Get NASA API Data for Near Earth Object Asteroids Tracking"""

    API = get(f"{BASE_URL}start_date={start_date}&end_date={end_date}&api_key={API_KEY}");
    if API.status_code == 200:
        return API.json();
    return None

def struct(near_earth_object, dates, element_key, object_type):
    """Add each Asteroid Data Structred into Dictionary"""
    
    obj_close_approach_data     = near_earth_object[dates[element_key]][object_type]['close_approach_data'][0]
    individual_asteroid_data    = get(near_earth_object[dates[element_key]][object_type]['links']['self']).json()
    asteroid        = near_earth_object[dates[element_key]][object_type]
    asteroid_info   = defaultdict(list)

    asteroid_info['id']                     = asteroid['id'];
    asteroid_info['name']                   = asteroid['name'];
    asteroid_info['hazardous']              = asteroid['is_potentially_hazardous_asteroid'];
    asteroid_info['close_approach_date']    = obj_close_approach_data['close_approach_date_full'];
    asteroid_info['current_orbiting_body']  = obj_close_approach_data['orbiting_body'];
    asteroid_info['diameter_meter']         = asteroid['estimated_diameter']['meters'];
    asteroid_info['diameter_feet']          = asteroid['estimated_diameter']['feet'];
    asteroid_info['velocity_km']            = obj_close_approach_data['relative_velocity']['kilometers_per_hour'];
    asteroid_info['velocity_miles']         = obj_close_approach_data['relative_velocity']['miles_per_hour'];
    asteroid_info['orbiting_bodies']        = asteroid_orbiting_bodies(individual_asteroid_data);
    asteroid_info['orbiting_class_type']    = asteroid_orbiting_type(individual_asteroid_data)['orbit_class_type'];
    asteroid_info['orbiting_type_description']  = asteroid_orbiting_type(individual_asteroid_data)['orbit_class_description'];
    asteroid_info['first_observation']          = asteroid_observation_dates(individual_asteroid_data)['first_observation_date'];
    asteroid_info['last_observation']           = asteroid_observation_dates(individual_asteroid_data)['last_observation_date'];

    return asteroid_info;

def get_info(near_earth_object, dates):
    """Get a list of informations about each Near Earth Object"""

    infoNEO = defaultdict(list)
    for element_key in range(len(dates)):
        for object_type in range(len(near_earth_object[dates[element_key]])):
            infoNEO[len(infoNEO)+1] = struct(near_earth_object, dates, element_key, object_type);
                
    return infoNEO;

def asteroid_orbiting_bodies(individual_asteroid_data):
    """Get each asteroid orbiting bodies"""

    passing_by_list = set()
    for i in range(len(individual_asteroid_data['close_approach_data'])):
        passing_by_list.add(individual_asteroid_data['close_approach_data'][i]['orbiting_body'])

    return passing_by_list;

def asteroid_orbiting_type(individual_asteroid_data):
    """Get each asteroid orbiting class"""
    
    orbit_class = individual_asteroid_data['orbital_data']['orbit_class'];

    return orbit_class;

def asteroid_observation_dates(individual_asteroid_data):
    """Get each asteroid observation dates"""

    observation_dates = individual_asteroid_data['orbital_data'];

    return observation_dates;

def print_neo_info(object_info):
    """Print the informations for each asteroid"""

    for asteroid in object_info:
            print(f"ASTEROID #{asteroid}")
            print(f"\t-ID -> {object_info[asteroid]['id']}")
            print(f"\t-Name -> {object_info[asteroid]['name']}")
            print(f"\t-Observation Dates:")
            print(f"\t\t*First -> {object_info[asteroid]['first_observation']}")
            print(f"\t\t*Last -> {object_info[asteroid]['last_observation']}")
            print(f"\t-Hazardous -> {object_info[asteroid]['hazardous']}")
            print(f"\t-Close Approach Date -> {object_info[asteroid]['close_approach_date']}")
            print(f"\t-Current Orbiting Body -> {object_info[asteroid]['current_orbiting_body']}")
            print(f"\t-Diametre:")
            print(f"\t\t*Min -> {int(object_info[asteroid]['diameter_meter']['estimated_diameter_min'])}m / {int(object_info[asteroid]['diameter_feet']['estimated_diameter_min'])}ft")
            print(f"\t\t*Max -> {int(object_info[asteroid]['diameter_meter']['estimated_diameter_max'])}m / {int(object_info[asteroid]['diameter_feet']['estimated_diameter_max'])}ft")
            print(f"\t-Relative Velocity:")
            print(f"\t\t*Km/h -> {object_info[asteroid]['velocity_km']}")
            print(f"\t\t*Miles/h -> {object_info[asteroid]['velocity_miles']}")
            print(f"\t-All Orbiting Bodies -> {object_info[asteroid]['orbiting_bodies']}")
            print(f"\t-Orbit Class Type:")
            print(f"\t\t*{object_info[asteroid]['orbiting_class_type']} -> {object_info[asteroid]['orbiting_type_description']}")
    
def start(BASE_URL, API_KEY, start_date, end_date):
    """Start the program"""

    data = get_data(BASE_URL, API_KEY, start_date, end_date);
    if data:
        num_of_object       = data["element_count"];
        near_earth_object   = data["near_earth_objects"];
        dates               = [];

        for i in range(int(start_date[-2:]), int(end_date[-2:])+1):
            dates.append(start_date[:-2]+"%02d" % int(str(i)));

        object_info = get_info(near_earth_object, dates);
        print_neo_info(object_info);
        
        print("\nNumber of Near Earth Object Detected ->", num_of_object);

    else:
        print("NEO Data No Found!");

def main():
    """Program Interfact"""

    os.system("cls || clear");
    print(
        """
        NASA ~ ASTEROIDS NeoWs 
    (Near Earth Object Web Service)
        """
    )

    timelapse   = input("ENTER TIMELAPSE -> [0 - 7] ");
    timelapse   = int(timelapse) if timelapse.isnumeric() else 0
    
    end_date    = (datetime.today()).strftime("%Y-%m-%d");
    start_date  = (datetime.today() - timedelta(days=timelapse)).strftime("%Y-%m-%d")
    
    BASE_URL    = "https://api.nasa.gov/neo/rest/v1/feed?";
    API_KEY     = ""; # --- your key API here --- #

    start(BASE_URL, API_KEY, start_date, end_date);


if __name__ == "__main__":
    main()
