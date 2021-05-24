from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

engine = create_engine("sqlite:///data/test.db")
Session = sessionmaker()
Session.configure(bind=engine)
session = Session()

hs = session.query("Hotspots")
print(hs.first())