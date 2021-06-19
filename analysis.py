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


def sp_index_from_name(session: Session, sp_name: str) -> int:
    q = session.query(Species).filter(Species.CommonName == sp_name).limit(1)
    return q.first().SpIndex


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
        self.hs_bv = "1" * len(loc_ids)
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
            self.sp_list = self.build_master_sp_list(init_session, self.observations)

    def trip_from_bv(self, bv: str) -> "Trip":
        pass

    @staticmethod
    def build_master_sp_list(session: Session, obs_dict: dict) -> list:
        """Returns a list of unique species in the all the hotspots in the Analysis in taxonomic order."""
        sp_set = set()
        for d in obs_dict.values():
            sp_set.update(d.keys())
        indicies = list(sp_set)
        indicies.sort(key=lambda sp: sp_index_from_name(session, sp))
        return indicies
        # indecies = [(sp, sp_index_from_name(session, sp)) for sp in sp_set]
        # indecies.sort(key=)

    @staticmethod
    def _bv_to_bools(bv: str) -> list:
        return [c == "1" for c in bv]

    #  Builtins
    def __len__(self):
        return len(self.hotspot_ids)

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

    # with Session() as this_session:
    #    print(hs_name_from_loc_id(this_session, PROSPECT_PARK))
    #    print(obs_dict_from_db(this_session, PROSPECT_PARK, 1))
    #    print(sp_index_from_name(this_session, "Common Ostrich"))

    test1 = Analysis([PROSPECT_PARK], 1, "test analysis")
    print(test1.observations)
