import csv
import json
import os

# from analysis import Analysis, Trip
from barchart import Barchart, Summary
from datetime import date
from functools import singledispatch
from pathlib import Path
from typing import Optional


class FileManager:
    EBIRD_BARCHART_FOLDER = R""
    BARCHART_FOLDER = Path(__file__) / "data" / "barcharts"
    SUMMARIES_FOLDER = R""
    ANALYSIS_FOLDER = R""

    BARCHART_FILENAME_ANATOMY = {
        "locid": 0,
        "timestamp": -1,
    }

    SUMMARY_FILENAME_ANATOMY = {
        "locid": 0,
        "period": 1,
        "timestamp": -1,
    }

    def __init__(self) -> None:
        # is it worth making this a singleton to prevent data races?
        pass

    @classmethod
    def is_current(cls, timestamp: str) -> bool:
        "Returns True if the supplied timestamp is from the current month. Otherwise returns False"
        today = cls.get_timestamp()
        deltas = cls.find_timestamp_delta(today, timestamp)
        return deltas[:2] == [0, 0]

    @staticmethod
    def get_timestamp() -> str:
        """Returns a timestamp string in the format 'yyyymmdd'."""
        return date.today().strftime("%Y%m%d")

    @classmethod
    def find_timestamp_delta(cls, timestamp_a: str, timestamp_b: str) -> list:
        """Returns the absolute difference between the year, month, and day values of 2 supplied timestamps as a list of ints."""
        ts_a = cls._ts_to_list(timestamp_a)
        ts_b = cls._ts_to_list(timestamp_b)
        diffs = []
        for a, b in zip(ts_a, ts_b):
            diffs.append(abs(a - b))
        return diffs

    @staticmethod
    def _ts_to_list(ts: str) -> list:
        """Takes a timestamp, and returns a list of ints for the year, month, and day components of the timestamp. Assumes yyyymmdd formatting."""
        return [int(ts[:4]), int(ts[4:6]), int(ts[6:])]

    @staticmethod
    def _ts_from_filename(filename: str) -> str:
        """Returns a timestamp string from a summplied filename. This assumes the filename ends with '_{timestamp}'"""
        ending = filename.split("_")[-1]
        if "." in ending:
            ts = ending.split(".")[0]
        else:
            ts = ending
        return ts

    @staticmethod
    def _loc_id_from_filename(filename: str) -> str:
        return filename.split("_")[0]

    @classmethod
    def get_most_recent_data_for_location(
        cls, loc_id: str, folder: str
    ) -> Optional[str]:
        files = cls.get_files_for_location(loc_id, folder)
        if not files:
            return None
        for i, file in enumerate(files):
            index = 0
            max = 0
            ts = int(cls._ts_from_filename(file))
            if ts > max:
                max = ts
                index = i
        return files[index]

    @classmethod
    def get_files_for_location(cls, loc_id: str, folder: str) -> list:
        files = []
        for file in cls.scan_files(Path(folder)):
            if cls._loc_id_from_filename(file) == loc_id:
                files.append(file)
        return files

    @staticmethod
    def _write_json(file_path: Path, file_name: str, json_string: str) -> None:
        full_path = Path(file_path) / file_name
        with open(full_path, "w") as out_file:
            json.dump(json_string, out_file)

    @staticmethod
    def scan_files(folder: str) -> list:
        for (_, _, files) in os.walk(folder):
            for f in files:
                yield f

    @classmethod
    def _file_exists_for_location(cls, loc_id: str, folder: str) -> bool:
        for f in cls.scan_files(Path(folder)):
            if cls._loc_id_from_filename(f) == loc_id:
                return True
        return False

    @classmethod
    def stash_barcart_json(cls, filename: str, json_string: str) -> None:
        loc_id = cls._loc_id_from_filename(filename)
        filename += ".json"
        most_recent_existing = cls.get_most_recent_data_for_location(
            loc_id, cls.BARCHART_FOLDER
        )
        if most_recent_existing and cls.is_current(
            cls._ts_from_filename(most_recent_existing)
        ):
            return None
        else:
            cls._write_json(cls.BARCHART_FOLDER, filename, json_string)


class FileNameMaker:
    def __init__(self) -> None:
        pass

    @singledispatch
    def make_filename(item):
        pass

    @make_filename.register
    def _(item: Barchart) -> str:
        filename = f"{item.loc_id}_barchart_{item.timestamp}"
        return filename

    @make_filename.register
    def _(item: Summary) -> str:
        filename = f"{item.loc_id}_summary_{item.period}_{item.timestamp}"
        return filename

    @make_filename.register
    def _(item: Analysis) -> str:
        filename = f"{item.title}_analysis_{item.period}"
        return filename

    @make_filename.register
    def _(item: Trip) -> str:
        filename = f"{item.title}_trip_{item.period}_{item.parks_bv}"
        return filename

    def parse_filename(filename: str) -> Optional[dict]:
        filetype = filename.split("_")[1]

    def _parse_summary_filename(filename) -> dict:
        fn_indeces = {"loc_id": 0, "peroid": 2, "timestamp": 3}
        parts = filename.split("_")
        outdict = {}
        for part, index in fn_indeces.items():
            outdict[part] = parts[index]
        return outdict

    def _parse_barchart_filename(filename) -> dict:
        pass

    def _parse_analysis_filename(filename) -> dict:
        pass

    def _parse_trip_filename(filename) -> dict:
        pass
