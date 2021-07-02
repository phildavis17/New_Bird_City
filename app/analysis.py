# from pathlib import Path
# import barchart as bc
# import file_manager as fm
# import eBird_interface as eb
import random
import uuid

from collections import defaultdict
from typing import Union

from sqlalchemy import create_engine
from sqlalchemy.orm import Session, raiseload, sessionmaker
from db_definitions import (
    Observation,
    Species,
    Hotspot,
    Period,
    AnalysisConfig,
    HotspotConfig,
)

ENGINE = create_engine("sqlite:///data/vagrant_db.db")
Session = sessionmaker()
Session.configure(bind=ENGINE)


def sp_name_from_index(session: Session, sp_index: int) -> str:
    """Returns the species name associated with the supplied species index in the databse."""
    q = session.query(Species).filter(Species.SpIndex == sp_index).limit(1)
    return q.first().CommonName


def sp_index_from_name(session: Session, sp_name: str) -> int:
    """Returns the species index associated with the supplied species name in the databse."""
    q = session.query(Species).filter(Species.CommonName == sp_name).limit(1)
    return q.first().SpIndex


def obs_dict_from_db(session: Session, loc_id: str, period: int) -> dict:
    """Returns a dict of observation data associated with the supplied loc id and period from the database."""
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
    """Returns the Hotspot name associated with the supplied loc id in the databse."""
    q = session.query(Hotspot).filter(Hotspot.LocId == loc_id).limit(1)
    return q.first().Name


def report_val(obs_val: float, precision=1) -> str:
    """
    Returns a the supplied Float or Int as a string followed by a '%'
    Special values are replaced with special strings
    """
    SPECIAL_CONDITIONS = {
        lambda x: x == 0: "-",
        lambda x: x < 0.01: "<1%",
        lambda x: x > 0.99: ">99%",
    }
    for condition, special_str in SPECIAL_CONDITIONS.items():
        if condition(obs_val):
            return special_str
    return f"{round(obs_val * 100, precision)}%"


def sort_dict_alpha(in_dict: dict):
    pass


def get_user_analyses(session: Session, username: str) -> dict:
    q = session.query(AnalysisConfig).filter(AnalysisConfig.UserId == username)
    analysis_dict = {}
    for config in q:
        analysis_dict[config.AnalysisName] = config.AnalysisId
    return analysis_dict


class Analysis:
    def __init__(self, loc_ids: list, period: int, name: str) -> None:
        self.hotspot_ids = tuple(sorted(loc_ids))
        self.user_id = (
            "DEMO_USER_001"  # FIXME: once user functionality is added, fix this.
        )
        self.analysis_id = uuid.uuid4()
        self.name = name
        self.period = period
        self.hs_is_active = {loc_id: True for loc_id in self.hotspot_ids}
        with Session() as init_session:
            self.observations = {
                loc_id: defaultdict(
                    float, obs_dict_from_db(init_session, loc_id, period)
                )
                for loc_id in loc_ids
            }
            self.hotspot_names = tuple(
                [
                    hs_name_from_loc_id(init_session, loc_id)
                    for loc_id in self.hotspot_ids
                ]
            )
            self.sp_list = self.build_master_sp_list(init_session)

    def trip_from_bv(self, bv: str) -> "Trip":
        """Returns a Trip object including or excluding hotspots based on the supplied bit vector string."""
        locs = [loc for loc, bit in zip(self.hotspot_ids, bv) if bit == "1"]
        pass

    def get_sp_obs(self, sp_name: str) -> dict:
        return {hs: self.observations[hs][sp_name] for hs in self.hotspot_ids}

    def build_master_sp_list(self, session: Session) -> list:
        """Returns a list of unique species in the all the hotspots in the Analysis in taxonomic order."""
        sp_list = list({key for o_dict in self.observations.values() for key in o_dict})
        return sorted(sp_list, key=lambda sp: sp_index_from_name(session, sp))

    def build_cumulative_obs_dict(self) -> dict:
        """
        Calculates the cumulative observation frequency for every species in all the hotspots set to active.
        """
        c_dict = {}
        for sp_name in self.sp_list:
            obs = 1
            for loc_id, val in self.get_sp_obs(sp_name).items():
                if not self.hs_is_active[loc_id]:
                    continue
                obs *= 1 - val
            c_dict[sp_name] = round(1 - obs, 5)
        return c_dict

    @classmethod
    def report_dict(cls, obs_dict: dict) -> dict:
        """
        Returns a version of the supplied dict with numeric values replaced with strings.
        Uses _report_val() to replace special values with special characters.
        """
        return {k: report_val(v) for k, v in obs_dict.items()}

    def _average_obs(self, sp_name: str, hs_included: set = None) -> float:
        """
        Calculates the average observation value for a supplied species and list of hotspots.
        If the list of hotspots is not included, will default to the Analysus objects full list.
        """
        # I've included the option to specify which hotspots to include in case I
        # decide I only want the average of the OTHER hotspots.
        if hs_included is None:
            hs_included = {hs for hs in self.hotspot_ids if self.hs_is_active[hs]}
        vals = [v for k, v in self.get_sp_obs(sp_name).items() if k in hs_included]
        return sum(vals) / len(vals)

    def _find_hs_specialties(self, loc_id: str) -> dict:
        """
        Returns a dictionary describing the extent to which the observation frequency of
        each species at a hotspot exceeds the average observation frequency among the
        other active hotspots, if such an excess exists.
        """
        other_hs = {hs for hs in self.hotspot_ids if self.hs_is_active[hs]}
        other_hs.discard(loc_id)
        return {
            sp: round(obs - self._average_obs(sp, other_hs), 5)
            for sp, obs in self.observations[loc_id].items()
            if obs > self._average_obs(sp, other_hs)
        }

    def build_specialties_dict(self) -> dict:
        """Returns a dict of specialties dicts for each active hotspot."""
        return {
            hs: self._find_hs_specialties(hs)
            for hs, active in self.hs_is_active.items()
            if active
        }

    def trip_dict_from_loc_ids(self, included_hs: Union[list, set]) -> dict:
        return {hs: obs for hs, obs in self.observations.items() if hs in included_hs}

    def trip_dict_from_bv(self, hs_bv: str) -> dict:
        if len(hs_bv) != len(self.hotspot_ids):
            raise ValueError(
                f"len of hotspot bit vector was {len(hs_bv)}. Expected {len(self.hotspot_ids)}."
            )
        # get from BV to

    @staticmethod
    def find_delta(obs_dict_a: dict, obs_dict_b: dict) -> dict:
        """Returns a dict describing the per-species difference in obs values between two Analysis objects."""
        # make a superset of sp names
        # calculate the difference between THIS obs and THAT obs
        sp_set = set(obs_dict_a.keys())
        sp_set.update(obs_dict_b.keys())
        sp_list = list(sp_set)
        sp_list.sort(key=sp_index_from_name)
        return {sp: obs_dict_a[sp] - obs_dict_b[sp] for sp in sp_list}

    @staticmethod
    def compare(obs_dict_a: dict, obs_dict_b: dict) -> list:
        """Splits a delta dict into two dicts,"""
        delta_dcit = Analysis.find_delta(obs_dict_a, obs_dict_b)
        a_dict = {sp: delta for sp, delta in delta_dcit if delta > 0}
        b_dict = {sp: delta for sp, delta in delta_dcit if delta < 0}
        return [a_dict, b_dict]

    @staticmethod
    def _bv_to_bools(bv: str) -> list:
        return [c == "1" for c in bv]

    @staticmethod
    def _bools_to_bv(bools: list) -> str:
        return "".join([str(int(b)) for b in bools])

    @staticmethod
    def simulate(obs_dict: dict) -> set:
        """Takes an observations dict and generates a"""
        seen_birds = set()
        for park_dict in obs_dict.values():
            seen_birds.update(
                {sp for sp, obs in park_dict.items() if obs > random.random()}
            )
        return seen_birds

    #  Builtins
    def __len__(self):
        return len(self.hotspot_ids)

    def __repr__(self):
        return f"Analysis Object '{self.name}' with {len(self)} hotspots."


class Trip:
    def __init__(self, obs_dict: dict, period) -> None:
        self.title = None  # TItle optional?
        self.period = None
        self.hotspots = None
        self.observations = {}
        self.specialties = self.build_specialties_dict(self.observations)

    def build_specialties_dict(self) -> dict:
        pass

    def simulate(self) -> set:
        """Simulates an outing, returning a set of species that are hits in the sim."""
        pass


if __name__ == "__main__":

    PROSPECT_PARK = "L109516"
    PLUMB_BEACH = "L444485"

    # with Session() as this_session:
    #    print(hs_name_from_loc_id(this_session, PROSPECT_PARK))
    #    print(obs_dict_from_db(this_session, PROSPECT_PARK, 1))
    #    print(sp_index_from_name(this_session, "Common Ostrich"))

    BKHS = [
        "L109145",
        "L109516",
        "L152773",
        "L285884",
        "L351189",
        "L385839",
        "L444485",
    ]
    bk = Analysis(BKHS, 17, "Brooklyn, baby")
    print(bk)
    # for park, obs in bk.observations.items():
    #    print(park)
    #    print(bk.report_dict(obs))
    # print(bk.report_dict(bk.get_sp_obs("Snow Goose")))
    # print(bk.report_dict(bk.build_cumulative_obs_dict()))
    # bk.hs_is_active[PROSPECT_PARK] = False
    # print(bk.report_dict(bk.build_cumulative_obs_dict()))
    # bk.hs_is_active[PROSPECT_PARK] = True
    # print("SPECIALTIES")
    # print("Prospect Park:")
    # print(bk._find_hs_specialties(PROSPECT_PARK))
    # print("Plumb Beach")
    # print(bk._find_hs_specialties(PLUMB_BEACH))
    # print(bk.simulate(bk.observations))
    for _ in range(10):
        print(len(bk.simulate(bk.observations)))
