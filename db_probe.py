from pathlib import Path
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from app.db_definitions import Observation, Species, Hotspot, Period

TARGET_DB = "NBC_DEV_DB.db"

engine = create_engine(f"sqlite:///data/{TARGET_DB}")
Session = sessionmaker()
Session.configure(bind=engine)
session = Session()

# hs name from locid
# locid from hs name (is this a good idea?)
# sp name from sp index
# sp index from sp name


def get_locid_from_hs_name(hs_name: str) -> str:
    hs = session.query(Hotspot).filter(Hotspot.Name == hs_name)
    return hs[0].LocId


def sp_name_from_index(sp_index: int) -> str:
    q = session.query(Species).filter(Species.SpIndex == sp_index)
    return q[0].CommonName


def obs_by_hs_period(hs_name: str, period_id: int) -> dict:
    obs_dict = {}
    loc_id = get_locid_from_hs_name(hs_name)
    obs = session.query(Observation).filter(
        Observation.PeriodId == period_id and Observation.LocId == loc_id
    )
    for ob in obs:
        obs_dict[sp_name_from_index(ob.SpIndex)] = ob.Obs
    return obs_dict


def obs_by_locid_period(loc_id: str, period: int) -> dict:
    obs_dict = {}
    q = (
        session.query(Observation)
        .filter(Observation.LocId == loc_id)
        .filter(Observation.PeriodId == period)
        .order_by(Observation.SpIndex)
    )
    for obs in q:
        obs_dict[sp_name_from_index(obs.SpIndex)] = obs.Obs
    return obs_dict


# print(obs_by_hs_period("Prospect Park", 17))

PROSPECT_PARK = "L109516"


def basic_probe():
    print(f"Species: {session.query(Species).first()}")
    print(f"Hotspot: {session.query(Hotspot).first()}")
    print(f"Period: {session.query(Period).first()}")
    print(f"Observation: {session.query(Observation).first()}")

def test_update_data():
    with Session() as sesh:
        hot = sesh.query(Period).first()
        print(hot)
        hot.PeriodId = 1000
        sesh.commit()
        hot_again = sesh.query(Period).first()
        print(hot_again)
        hot_again.PeriodId = 0
        sesh.commit()
        print(sesh.query(Period).filte)
    
def update_probe():
    with Session() as sesh:
        ps = sesh.query(Period).filter_by(Description = "Late December/Early January").one()
        ps.PeriodId = 0
        sesh.commit()
        for entry in sesh.query(Period):
            print(entry)
    
if __name__ == "__main__":
    #basic_probe()
    #test_update_data()
    update_probe()
