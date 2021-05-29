# Taxonomy
# place names
# periods


# --Taxonomy--
# Open the file
# make a class for every real bird

import csv
import barchart as bc
import logging

from pathlib import Path
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from db_definitions import Base, Observation, Species, Hotspot, Period

DB_PATH = Path(__file__).parent / "data" / "vagrant_db.db"
assert not DB_PATH.exists()
engine = create_engine("sqlite:///data/vagrant_db.db")

Base.metadata.create_all(engine)
Base.metadata.bind = engine
Session = sessionmaker()
Session.configure(bind=engine)
session = Session()

logging.basicConfig(level=logging.INFO)

# Periods
logging.info("Starting periods")
for p in range(48):
    this_period = Period()
    this_period.PeriodId = p
    this_period.Description = bc.Barchart.humanize_date_range(p)
    session.add(this_period)
session.commit()
logging.info("Periods done!")

# Taxonomy

TAXONOMY_PATH = Path(__file__).parent / "data" / "eBird_Taxonomy_v2019.csv"
TAXON_ORDER_COL = 0
CATEGORY_COL = 1  # This is the column that determines whether this is a Species or not.
CODE_COL = 2
COMMON_NAME_COL = 3
SCI_NAME_COL = 4

logging.info("Starting taxonomy.")
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
logging.info("Taxonomy done!")

# Demo Data Hotspots and observations
demo_dir = Path(__file__).parent / "data" / "demo" / "eBird Barchart Files"
# demo_dir = Path(__file__).parent / "data" / "testing" / "db_test"
eBird_files = list(demo_dir.glob("*/*.txt"))
logging.info("Starting hotspots")
for f in eBird_files:
    bar = bc.Barchart.new_from_csv(f)
    this_hotspot = Hotspot()
    this_hotspot.LocId = bar.loc_id
    this_hotspot.Name = bar.name
    this_hotspot.Timestamp = bar.timestamp
    session.add(this_hotspot)
session.commit()
logging.info("Hotspots done!")


# Observations
logging.info("Starting observations.")
for f in eBird_files:
    bar = bc.Barchart.new_from_csv(f)
    for p in range(48):
        summ_dict = bar.summarize_period(p)
        logging.debug(
            "building %s, period %s.",
            bar.name,
            str(p),
        )
        for sp, obs in summ_dict.items():
            sp_index = (
                session.query(Species).filter(Species.CommonName == sp)[0].SpIndex
            )
            this_obs = Observation()
            this_obs.PeriodId = p
            this_obs.SpIndex = sp_index
            this_obs.Obs = obs
            this_obs.LocId = bar.loc_id
            session.add(this_obs)
    session.commit()
    logging.info("%s done.", bar.name)
logging.info("Observations done!")
