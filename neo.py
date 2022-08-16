from collections import defaultdict
from requests import get
from datetime import datetime
import os


def get_data(BASE_URL, START_DATE, END_DATE, API_KEY):
    """Get NASA API Data for Near Earth Object Asteroids Tracking"""

    API = get(f"{BASE_URL}start_date={START_DATE}&end_date={END_DATE}&api_key={API_KEY}");
    if API.status_code == 200:
        return API.json();
    return None

def struct(NEO, DATES, element, object):
    """Near Earth Object Data Structred into Dictionary"""

    infoNEO = defaultdict(list)

    infoNEO['id'] = NEO[DATES[element]][object]['id'];
    infoNEO['name'] = NEO[DATES[element]][object]['name'];
    infoNEO['hazardous'] = NEO[DATES[element]][object]['is_potentially_hazardous_asteroid'];
    infoNEO['close_approach_date'] = NEO[DATES[element]][object]['close_approach_data'][0]['close_approach_date_full'];
    infoNEO['current_orbiting_body'] = NEO[DATES[element]][object]['close_approach_data'][0]['orbiting_body'];
    infoNEO['diameter_meter'] = NEO[DATES[element]][object]['estimated_diameter']['meters'];
    infoNEO['diameter_feet'] = NEO[DATES[element]][object]['estimated_diameter']['feet'];
    infoNEO['velocity_km'] = NEO[DATES[element]][object]['close_approach_data'][0]['relative_velocity']['kilometers_per_hour'];
    infoNEO['velocity_miles'] = NEO[DATES[element]][object]['close_approach_data'][0]['relative_velocity']['miles_per_hour'];
    infoNEO['orbiting_bodies'] = asteroid_orbiting_bodies(NEO, DATES, element, object);
    infoNEO['orbiting_class_type'] = asteroid_orbiting_type(NEO, DATES, element, object)[0];
    infoNEO['orbiting_type_description'] = asteroid_orbiting_type(NEO, DATES, element, object)[1];
    infoNEO['first_observation'] = asteroid_observation_dates(NEO, DATES, element, object)[0];
    infoNEO['last_observation'] = asteroid_observation_dates(NEO, DATES, element, object)[1];

    return infoNEO;


def get_info(NEO, DATES):
    """Get a list of informations about each Near Earth Object"""

    infoNEO = defaultdict(list)
    for element in range(len(DATES)):
        for object in range(len(NEO[DATES[element]])):
            infoNEO[len(infoNEO)+1] = struct(NEO, DATES, element, object);
                
    return infoNEO;

def asteroid_orbiting_bodies(NEO, DATES, element, object):
    """Get each asteroid orbiting bodies"""

    data = get(NEO[DATES[element]][object]['links']['self']).json()
    passing_by_list = set()
    for i in range(len(data['close_approach_data'])):
        passing_by_list.add(data['close_approach_data'][i]['orbiting_body'])

    return passing_by_list;

def asteroid_orbiting_type(NEO, DATES, element, object):
    """Get each asteroid orbiting type and description"""

    data = get(NEO[DATES[element]][object]['links']['self']).json();
    orbiting_type = defaultdict(list);
    orbiting_type[0] = data['orbital_data']['orbit_class']['orbit_class_type'];
    orbiting_type[1] = data['orbital_data']['orbit_class']['orbit_class_description'];

    return orbiting_type;

def asteroid_observation_dates(NEO, DATES, element, object):
    """Get asteroid first and last observation dates"""

    data = get(NEO[DATES[element]][object]['links']['self']).json()
    observation_dates = [0, 0];
    observation_dates[0] = data['orbital_data']['first_observation_date'];
    observation_dates[1] = data['orbital_data']['last_observation_date'];

    return observation_dates;

def print_info(object_info):
    """Print the informations for each NEO"""

    for i in object_info:
            print(
                f"ASTEROID #{i}",
                "\n\t-ID ->",object_info[i]['id'],
                "\n\t-Name ->", object_info[i]['name'],
                f"\n\t-Observation Dates:\n\t\t*First -> {object_info[i]['first_observation']}",
                                   f"\n\t\t*Last -> {object_info[i]['last_observation']}",
                "\n\t-Hazardous ->",object_info[i]['hazardous'],
                "\n\t-Close Approach Date ->",object_info[i]['close_approach_date'],
                "\n\t-Current Orbiting Body ->",object_info[i]['current_orbiting_body'],
                f"\n\t-Diametre:\n\t\t*Min -> {int(object_info[i]['diameter_meter']['estimated_diameter_min'])}m /", 
                                                     f"{int(object_info[i]['diameter_feet']['estimated_diameter_min'])}ft",
                                    f"\n\t\t*Max -> {int(object_info[i]['diameter_meter']['estimated_diameter_max'])}m /", 
                                                  f"{int(object_info[i]['diameter_feet']['estimated_diameter_max'])}ft",
                f"\n\t-Relative Velocity:\n\t\t*Km/h -> {object_info[i]['velocity_km']}",
                                   f"\n\t\t*Miles/h -> {object_info[i]['velocity_miles']}",
                "\n\t-All Orbiting Bodies ->", *object_info[i]['orbiting_bodies'],
                "\n\t-Orbit Class Type:\n\t\t*", object_info[i]['orbiting_class_type'],"->", object_info[i]['orbiting_type_description'],
            )
    
def start(BASE_URL, START_DATE, END_DATE, API_KEY):
    """Start the program"""

    data = get_data(BASE_URL, START_DATE, END_DATE, API_KEY);
    if data:
        num_of_object = data["element_count"];
        NEO = data["near_earth_objects"];
        DATES = [];

        for i in range(int(START_DATE[-2:]), int(END_DATE[-2:])+1):
            DATES.append(START_DATE[:-2]+"%02d" % int(str(i)));

        object_info = get_info(NEO, DATES);

        print_info(object_info);
        print("Number of Near Earth Object Detected ->", num_of_object);

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

    TIMELAPSE = int(input("ENTER TIMELAPSE -> [0 - 7] "));

    CURRENT_TIME = datetime.now();
    START_DATE = str(CURRENT_TIME.year)+ "-" +"%02d" % int(CURRENT_TIME.month) + "-" + "%02d" % int(CURRENT_TIME.day-TIMELAPSE);
    END_DATE = str(CURRENT_TIME.year)+ "-" +"%02d" % int(CURRENT_TIME.month) + "-" + "%02d" % int(CURRENT_TIME.day);

    BASE_URL = "https://api.nasa.gov/neo/rest/v1/feed?";
    API_KEY = ""; # --- your key API here --- #

    start(BASE_URL, START_DATE, END_DATE, API_KEY);


if "__name__" != "__main__":
    main()
