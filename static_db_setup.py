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
from uuid import uuid4
from analysis import Analysis
from db_definitions import (
    Base,
    Observation,
    Species,
    Hotspot,
    Period,
    User,
    AnalysisConfig,
    HotspotConfig,
)

DB_PATH = Path(__file__).parent / "data" / "vagrant_db.db"
assert not DB_PATH.exists()
engine = create_engine("sqlite:///data/vagrant_db.db")

Base.metadata.create_all(engine)
Base.metadata.bind = engine
Session = sessionmaker()
Session.configure(bind=engine)
session = Session()

logging.basicConfig(level=logging.INFO)
logging.info("Rebuilding database")
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

# Demo User
logging.info("User start")
demo_user = User()
demo_user.UserId = "Demo_User_001"
demo_user.Email = "***REMOVED***@gmail.com"
demo_user.LoginCount = 0
session.add(demo_user)
session.commit()
logging.info("User done!")

# Demo Analysis
logging.info("Demo Start")

BROOKLYN = [
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
    "L270814",
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

DEMO_ANALYSES = [
    (BROOKLYN, 18, "Demo - Brooklyn, May"),
    (AUSTIN, 25, "Demo - Austin, early July"),
    (BERMUDA, 30, "Demo - Bermuda, August"),
    (PHILADELPHIA, 18, "Demo - Philly, May"),
    (SEATTLE, 40, "Demo - Seattle, mid Autumn"),
    (SYDNEY, 0, "Demo - Sydney, new years"),
]

for a in DEMO_ANALYSES:
    locs, p, name = a
    a_id = str(uuid4())
    u_id = "Demo_User_001"
    this_a_config = AnalysisConfig()
    this_a_config.UserId = u_id
    this_a_config.AnalysisId = a_id
    this_a_config.AnalysisName = name
    this_a_config.PeriodId = p
    session.add(this_a_config)
    for loc in locs:
        this_hs_config = HotspotConfig()
        this_hs_config.UserId = u_id
        this_hs_config.AnalysisId = a_id
        this_hs_config.LocId = loc
        this_hs_config.IsActive = 1
        session.add(this_hs_config)
session.commit()
logging.info("Demo finished!")
