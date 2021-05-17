import csv
import json
from taxonomy_reader import CATEGORY_COL
from taxonomy_builder import COMMON_NAME_COL
import requests
import time

from pathlib import Path


class eBirdInterface:

    _API_KEY = "***REMOVED***"
    _HOTSPOT_INFOR_URL = "https://api.ebird.org/v2/ref/hotspot/info/"

    def __init__(self) -> None:
        pass

    @classmethod
    def get_hotspot_name(cls, loc_id: str) -> str:
        """Retrieves the name of the hotspot with the supplied loc_id from the eBird API and returns it as a string."""
        # Sleep for a second
        time.sleep(1)
        payload = {}
        headers = {
            "X-eBirdApiToken": cls._API_KEY,
        }
        url = cls._HOTSPOT_INFOR_URL + loc_id

        response_text = requests.request("GET", url, headers=headers, data=payload).text
        hs_dict = json.loads(response_text)
        return hs_dict["name"]


class TaxonomyLister:
    TAXONOMY_PATH = Path(__file__).parent / "data" / "eBird_Taxonomy_v2019.csv"
    TAXONOMY_JSON_PATH = Path(__file__).parent / "data" / "taxonomy.json"

    TAXON_ORDER_COL = 0
    CATEGORY_COL = (
        1  # This is the column that determines whether this is a Species or not.
    )
    COMMON_NAME_COL = 3
    SCI_NAME_COL = 4

    @classmethod
    def sort_by_taxon(cls, sp_list: list) -> list:
        sp_set = set(sp_list)
        sorted_list = []
        with open(cls.TAXONOMY_PATH, "r") as tax_file:
            reader = csv.reader(tax_file)
            for line in reader:
                cat = line[cls.CATEGORY_COL]
                sp = line[cls.COMMON_NAME_COL]
                if cat == "species" and sp in sp_set:
                    sorted_list.append()
        return sorted_list


if __name__ == "__main__":
    highbridge = "L2741553"
    cp = "L191106"

    print(eBirdInterface.get_hotspot_name(highbridge))
    print(eBirdInterface.get_hotspot_name(cp))
