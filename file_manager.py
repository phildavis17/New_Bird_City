import json
import logging
import os
import barchart as dt

from datetime import date
from pathlib import Path
from typing import Union

# from analysis import Analysis, Trip
# from barchart import Barchart, Summary


class FileManager:
    """
    This class provides utilities for finding, writing, and reading files.
    It is not intended to be instantiated.
    """

    #  EBIRD_BARCHART_FOLDER = Path(__file__).parent / "data" / "barcharts"  # This has not been standardized yet.

    DATA_FOLDERS = {
        "barchart": Path(__file__).parent / "data" / "barcharts",
        "summary": Path(__file__).parent / "data" / "summaries",
        "analysis": Path(__file__).parent / "data" / "analyses",
        "trip": Path(__file__).parent / "data" / "trips",
    }

    def __init__(self) -> None:
        pass

    @staticmethod
    def _scan_files(folder: str) -> list:
        """Yields the files in the supplied folder."""
        for (_, _, files) in os.walk(folder):
            for f in files:
                yield f

    @staticmethod
    def _pick_most_recent_file(file_list: list) -> str:
        """Returns the filename with the most recent timestamp from a list of supplied filenames."""
        if not file_list:
            raise ValueError("Empty list supplied")
        index = 0
        highest = 0
        for i, file in enumerate(file_list):
            ts = int(FileNameMaker.timestamp_from_filename(file))
            if ts > highest:
                highest = ts
                index = i
        return file_list[index]

    @staticmethod
    def _write_json(file_path: Path, file_name: str, json_string: str) -> None:
        file_name += ".json"
        full_path = Path(file_path) / file_name
        with open(full_path, "w") as out_file:
            json.dump(json_string, out_file)
            logging.info(f"json file written: {full_path}")

    @classmethod
    def _request_colliding_files(cls, folder: Path, target_dict: dict) -> list:
        """
        Returns a list of files in the supplied folder that collide with the supplied filename parts.
        Returns an empty list if none are found.
        """
        for part in target_dict:
            if part not in FileNameMaker.FN_PARTS:
                raise ValueError(f"Invalid Filename component: {part}")
        matching_files = []
        for filename in cls._scan_files(folder):
            if FileNameMaker.filename_collides(filename, target_dict):
                matching_files.append(filename)
        return matching_files

    @classmethod
    def _good_file_exists(cls, folder: Path, filename: str) -> bool:
        """Returns True if a file already exists covering the data that would be stored by a file with the supplied filename."""
        target_dict = FileNameMaker.parse_filename(filename)
        colliding_files = cls._request_colliding_files(folder, target_dict)
        if not colliding_files:
            return False
        #  If the file has a timestamp, it has to be current to be a conflict.
        if "timestamp" in target_dict:
            most_recent = cls._pick_most_recent_file(colliding_files)
            most_recent_timestamp = FileNameMaker.timestamp_from_filename(most_recent)
            return TimeKeeper.timestamp_is_current(most_recent_timestamp)
        return True

    @classmethod
    def stash_json(cls, filename: str, json_string: str) -> None:
        """Writes a JSON file to the appropriate folder, unless a good colliding filename is found."""
        file_type = FileNameMaker.parse_filename(filename)["type"]
        folder = cls.DATA_FOLDERS[file_type]
        if cls._good_file_exists(folder, filename):
            logging.info("Existing good file found. No file written.")
            return
        cls._write_json(folder, filename, json_string)


class TimeKeeper:
    """Provides utilities for creating and comparing timestamp strings."""

    def __init__(self) -> None:
        """
        TimeKeeper is a collection of static utility methods.
        It is not intended to be instantiated.
        """
        pass

    @staticmethod
    def generate_timestamp() -> str:
        """Returns a current timestamp string in ISO 8601 format 'YYYYMMDD'.
        NOTE: This should only be invoked for storage assignment during the creation of a new Barchart object.
        All other objects with timestamps get theirs from the Barchart from which they are derived."""
        return date.today().strftime("%Y%m%d")

    @staticmethod
    def _ts_to_list(ts: str) -> list:
        """Takes a timestamp, and returns a list of ints for the year, month, and day components of the timestamp. Assumes yyyymmdd formatting."""
        return [int(ts[:4]), int(ts[4:6]), int(ts[6:])]

    @classmethod
    def validate_timestamp(cls, timestamp: str) -> bool:
        """
        Returns True if supplied str conforms to rules for timestamps. Raises ValueError otherwise.

        RULES:
            - Must be 8 numeric characters.
            - Month portion must be greater than 0 and less than 13.
            - Day portion must be greater than 0 and less than 32.
        """
        rules = []
        rules.append(len(timestamp) == 8)
        rules.append(timestamp.isnumeric)
        ts_parts = cls._ts_to_list(timestamp)
        rules.append(0 < ts_parts[1] < 13)
        rules.append(0 < ts_parts[2] < 32)
        if not all(rules):
            raise ValueError(f"Improper Timestamp string: {timestamp}")
        return True

    @classmethod
    def timestamp_is_current(cls, timestamp: str) -> bool:
        "Returns True if the supplied timestamp is from the current month. Otherwise returns False"
        today = cls.generate_timestamp()
        deltas = cls._find_timestamp_delta(today, timestamp)
        return deltas[:2] == [0, 0]

    @classmethod
    def _find_timestamp_delta(cls, timestamp_a: str, timestamp_b: str) -> list:
        """Returns the absolute difference between the year, month, and day values of 2 supplied timestamps as a list of ints."""
        ts_a = cls._ts_to_list(timestamp_a)
        ts_b = cls._ts_to_list(timestamp_b)
        diffs = []
        for a, b in zip(ts_a, ts_b):
            diffs.append(abs(a - b))
        return diffs


class FileNameMaker:
    """Provides utilities for constructing and parsing file names."""

    FN_BLUEPRINTS = {
        "barchart": ("type", "loc_id", "timestamp"),
        "summary": ("type", "loc_id", "period", "timestamp"),
        "analysis": ("type", "title", "period"),
        "trip": ("type", "title", "period", "hs_bv"),
    }
    COLLISION_MATCH_PARTS = {
        "barchart": ("loc_id",),
        "summary": ("loc_id", "period"),
        "analysis": ("title",),
        "trip": ("title", "hs_bv"),
    }
    FN_PARTS = ("type", "loc_id", "title", "period", "timestamp", "hs_bv")
    SEPERATOR = "_"
    TYPE_INDEX = 0

    def __init__(self) -> None:
        pass

    @classmethod
    def _get_fn_identifiers(
        cls, item: Union["Barchart", "Summary", "Analysis", "Trip"]
    ) -> dict:
        """Returns a dict of the attributes used in that type's filename."""
        part_dict = {}
        part_dict["type"] = item.__class__.__name__.lower()
        for part in cls.FN_PARTS:
            if hasattr(item, part):
                part_dict[part] = getattr(item, part)
        return part_dict

    @classmethod
    def make_filename(
        cls, item: Union["Barchart", "Summary", "Analysis", "Trip"]
    ) -> str:
        """Returns a filename string that represents the supplied object."""
        parts_dict = cls._get_fn_identifiers(item)
        item_type = parts_dict["type"]
        fn_list = []
        template = cls.FN_BLUEPRINTS[item_type]
        for part in template:
            fn_list.append(str(parts_dict[part]))
        filename = cls.SEPERATOR.join(fn_list)
        cls._validate_filename(filename)
        return filename

    @classmethod
    def parse_filename(cls, filename: str) -> dict:
        """Returns a dict with supplied filename components mapped to the appropriate label."""
        filename = cls._strip_extension(filename)
        fn_parts = cls._unpack_filename(filename)
        item_type = fn_parts[cls.TYPE_INDEX]
        template = cls.FN_BLUEPRINTS[item_type]
        parts_dict = {}
        for part, value in zip(template, fn_parts):
            parts_dict[part] = value
        return parts_dict

    @classmethod
    def _strip_extension(cls, filename: str) -> str:
        """Returns a supplied file name string stripped of its extension, if one was present."""
        #  Only check the last part of the filename, in case a user has entered a period in the title of their analysis
        end = cls._unpack_filename(filename)[-1]
        if "." in end:
            return filename.rsplit(".", 1)[0]
        return filename

    @classmethod
    def _unpack_filename(cls, filename: str) -> list:
        return filename.split(cls.SEPERATOR)

    @classmethod
    def filename_matches(cls, filename, target_parts_dict: dict) -> bool:
        """Returns True if the supplied filename matches the specified parts."""
        file_parts = cls.parse_filename(filename)
        for part in target_parts_dict:
            if file_parts[part] != target_parts_dict[part]:
                return False
        return True

    @classmethod
    def filename_collides(cls, target_filename: str, check_parts: dict) -> bool:
        """Returns True if the """
        target_parts = cls.parse_filename(target_filename)
        file_type = target_parts["type"]
        for part in cls.COLLISION_MATCH_PARTS[file_type]:
            if check_parts[part] != target_parts[part]:
                return False
        return True

    @classmethod
    def _validate_filename(cls, filename: str) -> bool:
        """Returns True if the supplied filename conforms to naming conventions. Raises exceptions otherwise."""
        validator_methods = {
            "type": cls._validate_type,
            "loc_id": cls._validate_loc_id,
            "title": cls._validate_title,
            "period": cls._validate_period,
            "timestamp": TimeKeeper.validate_timestamp,
            "hs_bv": cls._validate_hs_bv,
        }
        fn_parts = cls.parse_filename(filename)
        checks = []
        for part, val in fn_parts.items():
            checks.append(validator_methods[part](val))
        return all(checks)

    @classmethod
    def _validate_type(cls, type_name: str) -> bool:
        """
        Returns True if supplied str conforms to rules for type identifiers. Raises ValueError otherwise.

        RULES: Must match one of the keys in the FileNameMaker object's FN_BLUEPRINTS attribute.
        """
        check = type_name in cls.FN_BLUEPRINTS
        if not check:
            raise ValueError(f"Improper Type identifier: {type_name}")
        return True

    @staticmethod
    def _validate_loc_id(loc_id):
        """Rules for eBird loc_id values are not well understood enough to validate. Returns True."""
        return True

    @staticmethod
    def _validate_title(title):
        """Rules for titles not yet defined. Returns True in the meantime."""
        # TODO: This behavior is not yet defined.
        return True

    @staticmethod
    def _validate_period(period: Union[str, int]) -> bool:
        """
        Returns True if supplied string or int conforms to rules for period identifiers. Raises ValueError otherwise.

        RULES: Must convert to an int within the range specified in the Barchart object's attribute.
        """
        check = int(period) in dt.Barchart.PERIODS
        if not check:
            raise ValueError(f"Improper Period identifier: {period}")
        return True

    @classmethod
    def _validate_hs_bv(cls, hs_bv: str) -> bool:
        """
        Returns True if supplied string conforms to rules for hotspot bit vectors. Raises ValueError otherwise.

        RULES: Must be a string, all characters are either "0" or "1".
        """
        valid_chars = ("0", "1")
        for c in hs_bv:
            if c not in valid_chars:
                raise ValueError(f"Improper hotspot bit vector value: {hs_bv}")
        return True

    @classmethod
    def _type_from_filename(cls, filename: str) -> str:
        """Returns the Type from the supplied filename."""
        return cls._unpack_filename(filename)[cls.TYPE_INDEX]

    @classmethod
    def _part_from_filename(cls, filename: str, part: str) -> str:
        if part not in cls.FN_PARTS:
            raise ValueError("Unhandled filename type.")
        fn_dict = cls.parse_filename(filename)
        return fn_dict[part]

    @classmethod
    def loc_id_from_filename(cls, filename) -> str:
        """Returns the loc_id from a supplied filename."""
        return cls._part_from_filename(filename, "loc_id")

    @classmethod
    def period_from_filename(cls, filename) -> str:
        """Returns the period from a supplied filename."""
        return cls._part_from_filename(filename, "period")

    @classmethod
    def timestamp_from_filename(cls, filename) -> str:
        """Returns the timestamp from a supplied filename."""
        return cls._part_from_filename(filename, "timestamp")

    @classmethod
    def title_from_filename(cls, filename) -> str:
        """Returns the loc_id from a supplied filename."""
        return cls._part_from_filename(filename, "title")

    @classmethod
    def hs_bv_from_filename(cls, filename) -> str:
        """Returns the loc_id from a supplied filename."""
        return cls._part_from_filename(filename, "hs_bv")


class Reporter:
    _THRESHOLD_HIGH = 0.99
    _THRESHOLD_LOW = 0.01

    def __init__(self) -> None:
        pass
