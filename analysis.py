from pathlib import Path
import barchart as bc
import file_manager as fm
import eBird_interface as eb
import uuid

from collections import defaultdict


from sqlalchemy import create_engine
from sqlalchemy.orm import Session, sessionmaker
from db_definitions import Observation, Species, Hotspot, Period, DBInterface

ENGINE = create_engine("sqlite:///data/vagrant_db.db")
Session = sessionmaker()
Session.configure(bind=ENGINE)


def sp_name_from_index(session: Session, sp_index: int) -> str:
    q = session.query(Species).filter(Species.SpIndex == sp_index).limit(1)
    return q.first().CommonName


def obs_dict_from_db(session: Session, loc_id: str, period: int) -> dict:
    obs_dict = {}
    q = (
        session.query(Observation)
        .filter(Observation.LocId == loc_id)
        .filter(Observation.PeriodId == period)
        .order_by(Observation.SpIndex)
    )
    for obs in q:
        obs_dict[sp_name_from_index(session, obs.SpIndex)] = obs.Obs
    return obs_dict


def hs_name_from_loc_id(session: Session, loc_id: str) -> str:
    q = session.query(Hotspot).filter(Hotspot.LocId == loc_id).limit(1)
    return q.first().Name


class Analysis:
    # WHAT AM I DOING????
    # Build Analysis
    # Modify BV
    # Sort Obs by

    def __init__(self, loc_ids: list, period: int, name: str) -> None:
        self.hotspot_ids = tuple(sorted(loc_ids))
        self.user_id = "DEMO_USER_001"
        self.analysis_id = uuid.uuid4()
        self.name = name
        self.period = period
        with Session() as init_session:
            self.observations = {
                loc_id: obs_dict_from_db(init_session, loc_id, period)
                for loc_id in loc_ids
            }
            self.hotspot_names = tuple(
                [
                    hs_name_from_loc_id(init_session, loc_id)
                    for loc_id in self.hotspot_ids
                ]
            )

        self.hs_bv = "1" * len(loc_ids)
        self.master_sp_list = []

    def trip_from_bv(self, bv: str) -> "Trip":
        pass

    def build_master_sp_list(session: Session, obs_dict: dict) -> list:
        sp_set = set()
        for d in obs_dict.values():
            sp_set.update(d.keys())
        #! This seems funky!
        indicies = [(sp, session.query(Species).filter(Species.CommonName))]

    @staticmethod
    def _bv_to_bools(bv: str) -> list:
        return [c == "1" for c in bv]

    #  Builtins
    def __len__(self):
        return len(self.hotspots)

    def __repr__(self):
        pass


class Trip:
    def __init__(self) -> None:
        self.title = ""
        self.period = None
        self.hs_bv = None
        self.hotspots = None
        self.observations = {}
        self.specialties = {}


PROSPECT_PARK = "L109516"

if __name__ == "__main__":

    with Session() as this_session:
        print(hs_name_from_loc_id(this_session, PROSPECT_PARK))
        print(obs_dict_from_db(this_session, PROSPECT_PARK, 1))
