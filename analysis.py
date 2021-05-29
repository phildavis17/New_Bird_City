from pathlib import Path
import barchart as bc
import file_manager as fm
import eBird_interface as eb

from collections import defaultdict


class Analysis:
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
        out_dict = {}
        paths = []
        
        for loc_id in loc_ids:
            new_file = fm.FileManager.request_best_file("barchart", {"loc_id": loc_id})
            if not new_file:
                raise ValueError(
                    f"No suitable file could be found for loc_id: {loc_id}"
                )
            paths.append(new_file)
        barcharts = []
        for file_path in paths:
            barcharts.append(bc.Barchart.new_from_json(file_path))
            
        obs_dicts = {}
        for chart in barcharts:
            pass
        
    def new_from_db(loc_ids: list, period: int, name: str, )

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
    
    def _ingest_summary(self, in_summary: "Summary") -> dict:
        pass

    @staticmethod
    def _bv_to_bools(bv: str) -> list:
        out_bools = []
        for c in bv:
            out_bools.append(c == "1")
        return out_bools

    #  Builtins
    def __len__(self):
        return len(self.hotspots)

    def __eq__(self, other):
        pass

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
