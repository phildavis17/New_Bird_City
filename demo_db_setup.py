import logging
import sqlalchemy

from analysis import Analysis

from pathlib import Path
from db_definitions import AnalysisConfig, HotspotConfig


BOOKLYN = [
    "L109145",
    "L109516",
    "L152773",
    "L285884",
    "L351189",
    "L385839",
    "L444485",
]

AUSTIN = [
    "L129127",
    "L270815",
    "L302109",
    "L436433",
    "L567534",
]

BERMUDA = [
    "L952649",
    "L2339599",
    "L2709029",
    "L2709162",
    "L2714552",
    "L2714557",
]

PHILADELPHIA = [
    "L160720",
    "L504403",
    "L1025768",
    "L1145863",
]

SEATTLE = [
    "L128138",
    "L128530",
    "L162766",
    "L165740",
    "L7497115",
]

SYDNEY = [
    "L915566",
    "L945869",
    "L958321",
    "L2444301",
]
