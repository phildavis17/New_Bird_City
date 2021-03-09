import calendar
import csv
import json
import math

from pathlib import Path

def get_period_columns(n: int) -> list:
    cols = []
    offset = 2
    for i in range(n - 2, n + 2):  #! this is a crazy way to set up this range. should be range(4) and offset gets you to the first good column.
        cols.append((i + offset) % (48 + offset))
    return cols


def humanize_date_range(n:int) -> str:
    """
    Returns a human readible description of the time period associated with the supplied int. Styled as follows:
    ...
    Late April
    Late April/Early May
    Early May
    Mid May
    Late May
    Late May/Early June
    Early June
    ...
    """
    qual = n % 4    
    if qual == 0:
        return f"{humanize_date_range(n - 1)}/{humanize_date_range(n + 1)}"
    
    month_str = calendar.month_name[math.ceil((n + 1) / 4)]
    if month_str == "":  # The calendar module has an extra empty string at index 0. This catches that.
        month_str = "December"
    
    qual_strs = {
        0: "",
        1: "Early",
        2: "Mid",
        3: "Late",
    }
    return f"{qual_strs[qual]} {month_str}"


def is_good_species(species):
    """Tests a supplied species name for substrings that indicate it is a sub-species level taxon."""
    flag_strings = [' sp.', ' x ', '/', 'Domestic']
    for flag in flag_strings:
        if flag.lower() in species.lower():
            return False
    return True




TEST_FILE = Path(R"C:\Users\Phil\Desktop\Buffer\ebird_L2741553__1900_2021_1_12_barchart.txt")

with open(TEST_FILE, 'r') as in_file:
    hotspot_file = csv.reader(in_file, dialect='excel-tab')
    