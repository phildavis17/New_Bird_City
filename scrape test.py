from bs4 import BeautifulSoup

import requests

URL = "https://ebird.org/barchart?r=L2741553&yr=all&m="
DOWNLOAD_URL = "https://ebird.org/barchartData?r=L2741553&bmo=1&emo=12&byr=1900&eyr=2021&fmt=tsv"
LOGIN_URL = "https://secure.birds.cornell.edu/cassso/login"
LOGIN_URL_2 = "https://secure.birds.cornell.edu/cassso/account/"


cookies = {
    "EBIRD_SESSIONID": "BE313069F30A1A10656987B08AE4D1AF"
}

data = {
    "username": "***REMOVED***",
    "password": "***REMOVED***",
}

#r = requests.get(DOWNLOAD_URL, cookies=cookies)
#soup = BeautifulSoup(r.content, 'html.parser')
#print(soup)

r = requests.post(LOGIN_URL_2, data=data)
soup = BeautifulSoup(r.content, "html.parser")
print(soup)

# ---=== NOTES ===---
# All we need to scrape the barchart data is a valid EBIRD_SESSIONID value, but how do we get it?

