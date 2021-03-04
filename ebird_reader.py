import calendar
import csv
import json
import math

def get_period_columns(n: int) -> list:
    cols = []
    offset = 2
    for i in range(n - 2, n + 2):
        cols.append((i + offset) % (48 + offset))
    return cols


def humanize_date_range(n:int) -> str:
    """
    Returns a human readible description of the time period associated with the supplied int. Styled as follows.
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



for i in range(48):
    print(humanize_date_range(i))
    
        


