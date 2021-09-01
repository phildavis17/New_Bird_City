"""
Utilities for retrieving information from eBird.
"""

import csv
import json
import requests
import time

from bs4 import BeautifulSoup
from pathlib import Path

from requests.models import Response

from config_secret import EBIRD_USERNAME, EBIRD_PASSWORD, EBIRD_HOTSPOT_API_URL, EBIRD_API_KEY, EBIRD_LOGIN_URL, EBIRD_BARCHART_URL_PARTS


#! Some kind of decent interval decorator!

def get_hotspot_name(loc_id: str) -> str:
    """Retrieves the name of the eBird hotspot with the supplied location ID."""
    time.sleep(1) #! this should be replaced by the decorator once done
    request_headers = {
        "X-eBirdApiToken": EBIRD_API_KEY,
    }
    url = EBIRD_HOTSPOT_API_URL + loc_id
    response = requests.get(url, headers=request_headers)
    hs_dict = json.loads(response)
    return hs_dict["name"]

def _latlong_str(n: float) -> str:
    """Returns the supplied float as a string with 2 decimal places, and signed if negative."""
    #? Maybe this should be removed, and the lat long info should be
    #? sanitized as they come from the map?
    return "{:.2f}".format(n)


def _fetch_nearby_hotspots(lat: float, long: float, distance: int = 25):
    """Fetches eBird hotspots within a specified distance to a supplied location."""
    # ---eBird API parameters---
    # Lat, long must be to 2 decimal places
    # distance is in KM, 0-50
    url = f"https://api.ebird.org/v2/ref/hotspot/geo?lat={_latlong_str(lat)}&lng={_latlong_str(long)}&dist={str(distance)}"
    request_headers = {
        "X-eBirdApiToken": EBIRD_API_KEY,
    }
    response = requests.get(url, headers=request_headers)
    reader = csv.reader(response.text.splitlines())
    return [row for row in reader]


def _filter_hotspot_list(raw_hotspots: list) -> list:
    """Takes a raw list of hotspot info from eBird and reduces it to loc_id, name, and sp count."""
    loc_id_col = 0
    name_col = 6
    sp_count_col = 8
    return [(row[loc_id_col], row[name_col], row[sp_count_col]) for row in raw_hotspots if len(row) == 9]
    # ^^^^ 
    # Some hotspots exist in eBird, but have never been visited and have no reported sightings
    # Since they have no sightings, their entries are only 7 items long
    # That's why this comprehension filters for lines that are 9 items long


def _n_best_hotspots(hs_list: list, n: int = 10) -> list:
    """Takes a filtered list of hotspots and returns a sorted list of a supplied length of the hotspots with the highest species count."""
    hs_list.sort(key = lambda x: int(x[2]))
    hs_list.reverse()
    return hs_list[:n]


def sort_by_taxon(sp_list: list) -> list:
    TAXONOMY_PATH = Path(__file__).parent / "data" / "eBird_Taxonomy_v2019.csv"
    CATEGORY_COL = 1
    COMMON_NAME_COL = 3
    
    sp_set = set(sp_list)
    sorted_list = []
    with open(TAXONOMY_PATH, "r") as tax_file:
        reader = csv.reader(tax_file)
        for line in reader:
            cat = line[CATEGORY_COL]
            sp = line[COMMON_NAME_COL]
            if cat == "species" and sp in sp_set:
                sorted_list.append(sp)
    return sorted_list


def fetch_hotspot_barchart(loc_id: str) -> list:
    """WARNING: This scrapes."""
    #! decorate with decent interval
    download_url = EBIRD_BARCHART_URL_PARTS[0] + loc_id + EBIRD_BARCHART_URL_PARTS[1]
    sesh = _get_logged_in_session()
    time.sleep(5)
    text_file = sesh.get(download_url).text
    csv_reader = csv.reader(text_file.split("\n"), dialect="excel-tab")
    return [row for row in csv_reader]


def _get_logged_in_session() -> "requests.Session":
    """Returns a requests session that is logged in to ebird."""
    with requests.Session() as sesh:
        r = sesh.get(EBIRD_LOGIN_URL)
        sesh.post(EBIRD_LOGIN_URL, data = _build_ebird_login_payload(r))
    return sesh


def _build_ebird_login_payload(web_response: "requests.Response") -> dict:
    """Constructs the appropriate payload for login including the hidden fields."""
    payload = {
        "username": EBIRD_USERNAME,
        "password": EBIRD_PASSWORD,
    }
    important_tags = {"lt", "execution", "_eventId"}
    soup = BeautifulSoup(web_response.text, "html.parser")
    tags = soup.find_all("input", type="hidden")
    for tag in tags:
        if tag["name"] in important_tags:
            payload[tag["name"]] = tag["value"]
    return payload


if __name__ == "__main__":
    #print(fetch_hotspot_barchart("L952649"))
    NYC_LAT = 40.71
    NYC_LONG = -74.00
    hotspots = _fetch_nearby_hotspots(NYC_LAT, NYC_LONG, 10)
    print(_n_best_hotspots(_filter_hotspot_list(hotspots), 10))
