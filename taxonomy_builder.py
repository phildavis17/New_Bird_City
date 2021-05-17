"""
This is a script to build/rebuild a list of species level taxa in the eBird Taxonomy.
"""

import csv
import json

from pathlib import Path

TAXONOMY_PATH = Path(__file__).parent / "data" / "eBird_Taxonomy_v2019.csv"
TAXON_ORDER_COL = 0
CATEGORY_COL = 1  # This is the column that determines whether this is a Species or not.
COMMON_NAME_COL = 3
SCI_NAME_COL = 4

TAXONOMY_JSON_PATH = Path(__file__).parent / "data" / "taxonomy.json"

TAXON_LIST = []
with open(TAXONOMY_PATH, "r") as tax_file:
    reader = csv.reader(tax_file)
    for line in reader:
        tax_dict = {}
        if line[CATEGORY_COL] == "species":
            TAXON_LIST.append(line[COMMON_NAME_COL])

with open(TAXONOMY_JSON_PATH, "w") as tax_json:
    json.dump(TAXON_LIST, tax_json)
