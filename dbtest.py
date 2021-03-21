from db_definitions import Species, Hotstpot, Period, User, Observation, Analysis, HotspotConfig, SeenBird
from sqlalchemy import engine, create_engine
from sqlalchemy.orm import sessionmaker

engine = create_engine('sqlite:///data/test.db')

DBSession = sessionmaker(bind=engine)
session = DBSession()

sp = session.query(Species).first()
print(sp.CommonName)