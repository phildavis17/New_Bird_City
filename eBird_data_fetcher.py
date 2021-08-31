"""
Utilities for retrieving information from eBird.
"""

import csv
import json
import requests
import time

from bs4 import BeautifulSoup
from pathlib import Path

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
    with requests.Session() as sesh:
        r = sesh.get(EBIRD_LOGIN_URL)
        sesh.post(EBIRD_LOGIN_URL, data = _build_ebird_login_payload(r))
    return sesh


def _build_ebird_login_payload(web_response: "requests.Response") -> dict:
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
    print(fetch_hotspot_barchart("L952649"))