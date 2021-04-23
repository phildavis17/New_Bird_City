import json
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


if __name__ == "__main__":
    highbridge = "L2741553"
    cp = "L191106"

    print(eBirdInterface.get_hotspot_name(highbridge))
    print(eBirdInterface.get_hotspot_name(cp))