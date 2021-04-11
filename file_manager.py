import csv
import json
import os

from analysis import Analysis, Trip
from barchart import Barchart, Summary
from datetime import date
from functools import singledispatch
from pathlib import Path
from typing import Optional


class FileManager:
    """Provides utilities for writing and reading files."""

    #  EBIRD_BARCHART_FOLDER = Path(__file__).parent / "data" / "barcharts"  # This has not been standardized yet.
    BARCHART_FOLDER = Path(__file__).parent / "data" / "barcharts"
    SUMMARIES_FOLDER = Path(__file__).parent / "data" / "summaries"
    ANALYSIS_FOLDER = Path(__file__).parent / "data" / "analyses"
    TRIPS_FOLDER = Path(__file__).parent / "data" / "trips"

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
        """Returns a current timestamp string in the format 'yyyymmdd'.
        NOTE: This should only be invoked during the creation of a new Barchart object.
        All other objects with timestamps get theirs from the Barchart from which they are derived."""
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

    @classmethod
    def get_most_recent_data_for_location(
        cls, loc_id: str, folder: str
    ) -> Optional[str]:
        """Returns the filename of the most recent file for the supplied loc id in the supplied folder. Returns None if no such file is found."""
        files = cls.get_files_for_location(loc_id, folder)
        if not files:
            return None
        index = 0
        max = 0
        for i, file in enumerate(files):
            ts = int(FileNameMaker.timestamp_from_filename(file))
            if ts > max:
                max = ts
                index = i
        return files[index]

    @classmethod
    def get_files_for_location(cls, loc_id: str, folder: str) -> list:
        files = []
        for file in cls.scan_files(Path(folder)):
            if FileNameMaker.loc_id_from_filename(file) == loc_id:
                files.append(file)
        return files

    @staticmethod
    def _write_json(file_path: Path, file_name: str, json_string: str) -> None:
        full_path = Path(file_path) / file_name
        with open(full_path, "w") as out_file:
            json.dump(json_string, out_file)

    @staticmethod
    def scan_files(folder: str) -> list:
        """Yields the files in the supplied folder."""
        for (_, _, files) in os.walk(folder):
            for f in files:
                yield f

    @classmethod
    def stash_barcart_json(cls, filename: str, json_string: str) -> None:
        """Saves a json file if a current file for that location is not present. If there is a current file, does nothing."""
        #! Should this return something to report whether or not it saved something?
        loc_id = FileNameMaker.loc_id_from_filename(filename)
        most_recent_existing = cls.get_most_recent_data_for_location(
            loc_id, cls.BARCHART_FOLDER
        )
        if most_recent_existing and cls.is_current(
            FileNameMaker.timestamp_from_filename(most_recent_existing)
        ):
            return None
        else:
            filename += ".json"
            cls._write_json(cls.BARCHART_FOLDER, filename, json_string)

    @classmethod
    def stash_summary_json(cls, filename: str, json_string: str) -> None:
        pass

    @classmethod
    def stash_json(cls, filename: str, json_string: str) -> None:
        # Barchart: write if no current file
        # Summary: Write if no current file
        # Analysis: Overwrite. All that changes is the bitvector (should these even be written, then???)
        # Trip: Static, I think. write if none present.
        pass


class FileNameMaker:
    """Provides utilities for constructing and parsing file names."""

    FN_INDECES = {
        "barchart": {"loc_id": 0, "timestamp": -1},
        "summary": {"loc_id": 0, "peroid": 2, "timestamp": -1},
        "analysis": {"title": 0, "period": -1},
        "trip": {"title": 0, "period": 2, "hs_bv": -1},
    }

    SEPERATOR = "_"
    TYPE_INDEX = 1

    def __init__(self) -> None:
        pass

    @singledispatch
    @staticmethod
    def make_filename(item):
        raise NotImplementedError(f"Unhandled type{type(item)}")

    @make_filename.register(Barchart)
    @staticmethod
    def _(item: Barchart) -> str:
        filename = f"{item.loc_id}_barchart_{item.timestamp}"
        return filename

    @make_filename.register(Summary)
    @staticmethod
    def _(item: Summary) -> str:
        filename = f"{item.loc_id}_summary_{item.period}_{item.timestamp}"
        return filename

    @make_filename.register(Analysis)
    @staticmethod
    def _(item: Analysis) -> str:
        filename = f"{item.title}_analysis_{item.period}"
        return filename

    @make_filename.register(Trip)
    @staticmethod
    def _(item: Trip) -> str:
        filename = f"{item.title}_trip_{item.period}_{item.hs_bv}"
        return filename

    @classmethod
    def _strip_extension(cls, filename: str) -> str:
        """Returns a supplied file name string stripped of its extension, if one was present."""
        #  Only check the last part of the filename, in case a user has entered a period in the title of their analysis
        end = cls._break_filename[-1]
        if "." in end:
            return filename.rsplit(".", 1)[0]
        return filename

    @classmethod
    def _break_filename(cls, filename: str) -> list:
        return filename.split(cls.SEPERATOR)

    @classmethod
    def parse_filename(cls, filename: str) -> Optional[dict]:
        filename = cls._strip_extension(filename)
        fn_parts = cls._break_filename(filename)
        object_type = fn_parts[cls.TYPE_INDEX]
        if object_type not in cls.FN_INDECES:
            raise NotImplementedError(f"Unhandled object type {object_type}")
        fn_dict = {}
        for part, index in cls.FN_INDECES[object_type].items():
            fn_dict[part] = fn_parts[index]
        return fn_dict

    @classmethod
    def _part_from_filename(cls, filename: str, part: str) -> Optional[str]:
        fn_dict = cls.parse_filename(filename)
        return fn_dict[part]

    @classmethod
    def loc_id_from_filename(cls, filename) -> str:
        return cls._part_from_filename(filename, "loc_id")

    @classmethod
    def period_from_filename(cls, filename) -> str:
        return cls._part_from_filename(filename, "period")

    @classmethod
    def timestamp_from_filename(cls, filename) -> str:
        ts = cls._part_from_filename(filename, "timestamp")
        return ts

    @classmethod
    def title_from_filename(cls, filename) -> str:
        return cls._part_from_filename(filename, "title")

    @classmethod
    def hs_bv_from_filename(cls, filename) -> str:
        return cls._part_from_filename(filename, "hs_bv")