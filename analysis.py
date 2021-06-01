from pathlib import Path
import barchart as bc
import file_manager as fm
import eBird_interface as eb

from collections import defaultdict


from sqlalchemy import create_engine
from sqlalchemy.orm import Session, sessionmaker
from db_definitions import Observation, Species, Hotspot, Period, DBInterface

ENGINE = create_engine("sqlite:///data/vagrant_db.db")
# Session = sessionmaker()
# Session.configure(bind=engine)
# this_session = Session()


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
        self.title = name
        self.period = period
        self.hotspot_ids = tuple(sorted(loc_ids))
        self.hotspot_names = self._get_hotspot_names(self.hotspot_ids)
        self.hs_bv = "1" * len(loc_ids)
        self.observations = self._build_obs_dict(self.hotspots, self.period)
        self.master_sp_list = []

    def _build_obs_dict(loc_ids: list, period: int) -> dict:
        pass

    def _get_hotspot_names(loc_ids: tuple) -> dict:
        """Returns a dict with supplied loc_ids as keys and matching hotspot names as values."""
        hs_name_dict = {}
        for loc_id in loc_ids:
            hs_name_dict[loc_id] = eb.eBirdInterface.get_hotspot_name(loc_id)
        return hs_name_dict

    def _build_summaries(loc_ids: list, period: int) -> list:
        pass

    # get best file for locID
    # make a new barchart from it
    # get a period summary dict from that Barchart
    # ingest the period summary dict
    # ingest summary

    def trip_from_bv(self, bv: str) -> "Trip":
        pass

    def _ingest_obs_dict(self, in_dict: dict) -> dict:
        obs_dict = defaultdict(float)
        obs_dict.update(in_summary.observations)
        out_dict = {in_loc: obs_dict}
        return out_dict

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
    print(hs_name_from_loc_id(PROSPECT_PARK))
    print(obs_dict_from_db(PROSPECT_PARK, 1))