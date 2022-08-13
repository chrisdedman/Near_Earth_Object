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

def get_info(NEO, DATES):
    """Get a list of name of Near Earth Object"""
    infoNEO = defaultdict(list)
    for element in range(len(DATES)):
        for object in range(len(NEO[DATES[element]])):
            infoNEO[object+1] = [
                    NEO[DATES[element]][object]['id'],
                    NEO[DATES[element]][object]['name'],
                    NEO[DATES[element]][object]['is_potentially_hazardous_asteroid'],
                    NEO[DATES[element]][object]['close_approach_data'][0]['close_approach_date_full'],
                    NEO[DATES[element]][object]['close_approach_data'][0]['orbiting_body'],
                    NEO[DATES[element]][object]['estimated_diameter']['meters'],
                    NEO[DATES[element]][object]['estimated_diameter']['feet'],
                    NEO[DATES[element]][object]['close_approach_data'][0]['relative_velocity']['kilometers_per_hour'],
                    NEO[DATES[element]][object]['close_approach_data'][0]['relative_velocity']['miles_per_hour'],
                    asteroid_orbiting_bodies(NEO, DATES, element, object)
                ]

    return infoNEO;

def print_info(object_info):
    """Print the informations for each NEO"""

    for i in object_info:
            print(
                f"Object #{i}",
                "\n\t-ID ->",object_info[i][0],
                "\n\t-Name ->", object_info[i][1],
                "\n\t-Hazardous ->",object_info[i][2],
                "\n\t-Close Approach Date ->",object_info[i][3],
                "\n\t-Current Orbiting Body ->",object_info[i][4],
                f"\n\t-Diametre Meter:\n\t\t*Min -> {int(object_info[i][5]['estimated_diameter_min'])}m",
                                    f"\n\t\t*Max -> {int(object_info[i][5]['estimated_diameter_max'])}m",
                f"\n\t-Diameter Feet:\n\t\t*Min -> {int(object_info[i][6]['estimated_diameter_min'])}ft",
                                   f"\n\t\t*Max -> {int(object_info[i][6]['estimated_diameter_max'])}ft",
                f"\n\t-Relative Velocity:\n\t\t*Km/h -> {object_info[i][7]}",
                                   f"\n\t\t*Miles/h -> {object_info[i][8]}",
                "\n\t-All Orbiting Bodies ->", object_info[i][9],
                                   '\n'
            )

def asteroid_orbiting_bodies(NEO, DATES, element, object):
    """Get each asteroid orbiting bodies"""

    data = get(NEO[DATES[element]][object]['links']['self']).json()
    passing_by_list = set()
    for i in range(len(data['close_approach_data'])):
        passing_by_list.add(data['close_approach_data'][i]['orbiting_body'])
    return passing_by_list;


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
        print("Data No Found!");

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
