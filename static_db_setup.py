# Taxonomy
# place names
# periods


# --Taxonomy--
# Open the file
# make a class for every real bird

import barchart as bc

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from db_definitions import Species, Hotstpot, Period


engine = create_engine("sqlite:///data/test.db")


Session = sessionmaker()
Session.configure(bind=engine)
session = Session()

for p in range(49):
    this_period = Period()
    this_period.PeriodId = p
    this_period.Description = bc.Barchart.humanize_date_range()
    session.add(this_period)

print(session.new)
session.commit()