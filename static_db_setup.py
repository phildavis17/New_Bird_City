# Taxonomy
# place names
# periods


# --Taxonomy--
# Open the file
# make a class for every real bird

import csv
import barchart as bc
import sqlite3

from pathlib import Path
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from db_definitions import Base, Species, Hotstpot, Period
from eBird_interface import eBirdInterface

DB_PATH = Path(__file__).parent / "data" / "test.db"

assert not DB_PATH.exists()


engine = create_engine("sqlite:///data/test.db")


Base.metadata.create_all(engine)
Base.metadata.bind = engine
Session = sessionmaker()
Session.configure(bind=engine)
session = Session()

# Periods
for p in range(48):
    this_period = Period()
    this_period.PeriodId = p
    this_period.Description = bc.Barchart.humanize_date_range(p)
    session.add(this_period)

session.commit()

# Taxonomy
TAXONOMY_PATH = Path(__file__).parent / "data" / "eBird_Taxonomy_v2019.csv"
TAXON_ORDER_COL = 0
CATEGORY_COL = 1  # This is the column that determines whether this is a Species or not.
CODE_COL = 2
COMMON_NAME_COL = 3
SCI_NAME_COL = 4

with open(TAXONOMY_PATH, "r") as tax_file:
    reader = csv.reader(tax_file)
    for line in reader:
        tax_dict = {}
        if line[CATEGORY_COL] == "species":
            this_species = Species()
            this_species.SpIndex = line[TAXON_ORDER_COL]
            this_species.CommonName = line[COMMON_NAME_COL]
            this_species.SpCode = line[CODE_COL]
            this_species.SciName = line[SCI_NAME_COL]
            session.add(this_species)
session.commit()

# Demo Data Hotspots
demo_dir = Path(__file__).parent / "data" / "demo" / "eBird Barchart Files"
for f in demo_dir.glob("*/*.txt"):
    bar = bc.Barchart.new_from_csv(f)
    this_hotspot = Hotstpot()
    this_hotspot.LocId = bar.loc_id
    this_hotspot.Name = eBirdInterface.get_hotspot_name(this_hotspot.LocId)
    this_hotspot.Timestamp = bar.timestamp
    session.add(this_hotspot)
session.commit()
