"""
Barchart objects are used to hold barcart data from eBird. Summary objects hold data summarizing their parent barcarts for a specific period.
"""

import calendar
import csv
import json
import logging
import math
from os import stat
import file_manager as fm  # Aliased to prevent circular import
import eBird_data_fetcher as eb

from pathlib import Path


class Barchart:
    BC_FILE_COL_OFFSET = (
        -2
    )  # This is the offset to get the correct columns from eBird barchart files.
    BC_FILE_SAMP_SIZE_ROW = 14
    BC_FILE_OBS_START_ROW = 16
    PERIODS = tuple(range(48))

    def __init__(self) -> None:
        self.timestamp = fm.TimeKeeper.generate_timestamp()
        self.loc_id = ""
        self.name = ""
        self.samp_sizes = []
        self.observations = {}

    @staticmethod
    def new_from_csv(csv_path):
        """Returns a new Barchart object containing the data from the specified .csv file."""
        row_data = Barchart._read_csv_file(csv_path)
        new_barchart = Barchart()
        new_barchart.ingest_csv_data(row_data)
        new_barchart.loc_id = Barchart.loc_id_from_ebird_barchart(csv_path)
        return new_barchart

    def ingest_csv_data(self, row_list: list) -> None:
        """Populates Barchart data from a provided eBird barchart file."""
        samps = [int(float(x)) for x in row_list[self.BC_FILE_SAMP_SIZE_ROW][1:] if x]
        obs = {}
        for row in self.filter_observation_rows(row_list[self.BC_FILE_OBS_START_ROW :]):
            sp_name = self.clean_sp_name(row[0])
            obs[sp_name] = [float(x) for x in row[1:] if x]
        #self.loc_id = self.loc_id_from_ebird_barchart(csv_path)
        self.samp_sizes = samps
        self.observations = obs
        self._get_name()

    @staticmethod
    def new_from_ebird_fetch(loc_id: str) -> "Barchart":
        """Returns a new Barchart object containing data from a CSV direct from ebird."""
        new_barchart = Barchart()
        new_barchart.ingest_csv_data(eb.fetch_hotspot_barchart(loc_id))
        new_barchart.loc_id = loc_id
        return new_barchart


    def _get_name(self):
        """Gives itself a Name attribute."""
        if not self.loc_id:
            raise ValueError("Name requested with no loc_id value")
        if hasattr(self, "name") and self.name:
            logging.info("Barchart object already has name.")
            return
        self.name = eb.get_hotspot_name(self.loc_id)

    @staticmethod
    def _read_csv_file(csv_path: Path) -> list:
        """Returns a the lines of an eBird Barchart File as a list. Does no filtering."""
        with open(csv_path, "r") as in_file:
            row_list = []
            reader = csv.reader(in_file, dialect="excel-tab")
            for row in reader:
                row_list.append(row)
        return row_list

    @classmethod
    def filter_observation_rows(cls, raw_rows: list) -> list:
        """Returns a list of only the supplied rows that begin with an accepted species name."""
        filtered = []
        for row in raw_rows:
            if row and cls.is_good_species(cls.clean_sp_name(row[0])):
                filtered.append(row)
        return filtered

    @staticmethod
    def loc_id_from_ebird_barchart(csv_path: Path) -> str:
        """
        Returns the location ID of a hotspot from an eBird bar chart file name. Assumes file has not been renamed.
        Differs from similar method in FileManager, as it deals with eBird files, not files named by this app.
        """
        return csv_path.stem.split("_")[1]

    @staticmethod
    def new_from_json(json_path: Path):
        """Returns a new Barchart object with data from a supplied JSON file."""
        new_barchart = Barchart()
        new_barchart.ingest_json(json_path)
        return new_barchart

    def ingest_json(self, json_path: Path) -> None:
        """Reads the data from a JSON file, and populates a Barchart with it."""
        json_string = self._read_json_file(json_path)
        in_dict = json.loads(json_string)
        self.loc_id = in_dict["loc_id"]
        self.timestamp = in_dict["timestamp"]
        self.samp_sizes = in_dict["samp_sizes"]
        self.observations = in_dict["observations"]

    @staticmethod
    def _read_json_file(json_path: Path) -> str:
        with open(json_path, "r") as in_file:
            json_string = json.load(in_file)
        return json_string

    def _to_json_string(self) -> str:
        """Creates a json compatable string representation of this Barchart object."""
        out_dict = {}
        out_dict["loc_id"] = self.loc_id
        out_dict["timestamp"] = self.timestamp
        out_dict["samp_sizes"] = self.samp_sizes
        out_dict["observations"] = self.observations
        return json.dumps(out_dict)

    @classmethod
    def get_period_columns(cls, n: int) -> list:
        cols = []
        for i in range(4):
            col = (n + i + cls.BC_FILE_COL_OFFSET) % 48
            cols.append(col)
        return cols

    @staticmethod
    def humanize_date_range(n: int) -> str:
        """
        Returns a human readible description of the time period associated with the supplied int. Styled as follows:
        ...
        Late April
        Late April/Early May
        Early May
        Mid May
        Late May
        Late May/Early June
        Early June
        ...
        """
        qual = n % 4
        if qual == 0:
            return f"{Barchart.humanize_date_range(n - 1)}/{Barchart.humanize_date_range(n + 1)}"

        month_str = calendar.month_name[math.ceil((n + 1) / 4)]
        if month_str == "":
            month_str = "December"  # The calendar module has an extra empty string at index 0. This catches that.

        qual_strs = {
            0: "",
            1: "Early",
            2: "Mid",
            3: "Late",
        }
        return f"{qual_strs[qual]} {month_str}"

    @staticmethod
    def is_good_species(species: str) -> bool:
        """Tests a supplied species name for substrings that indicate it is a sub-species level taxon."""
        flag_strings = (" sp.", " x ", "/", "Domestic", "hybrid")
        for flag in flag_strings:
            if flag.lower() in species.lower():
                return False
        return True

    @staticmethod
    def clean_sp_name(sp_name: str) -> str:
        """Removes scientific name from species name cell if present."""
        # At time of writing, scientific names are all preceded by " (<".
        # If eBird changes this, this method will break.
        end_index = sp_name.find(" (<")
        if end_index == -1:
            return sp_name
        return sp_name[:end_index]

    @staticmethod
    def combined_average(samp_sizes: list, obs: list) -> float:
        """Takes two lists of numbers and returns the combined average as a float.

        Args:
            samp_size: A list  of sample sizes as floats.
            presence: A list of occurance data as floats.

        Returns:
            The combined average as a float

        Raises:
            IndexError: The function will give unexpected results if the lists are
            of different lengths, so it raises an IndexError rather than failing silently.
        """
        if not len(samp_sizes) == len(obs):
            raise IndexError("Lists must have the same length.")
        total_num_present = 0
        data = zip(samp_sizes, obs)
        for pair in data:
            total_num_present += round(pair[0] * pair[1])
        if sum(samp_sizes) == 0:
            return 0.0
        return round(total_num_present / sum(samp_sizes), 5)

    def get_observation(self, sp_name: str, index: int) -> float:
        """
        Returns the obervation of a supplied species for a supplied column number.
        Provides a more readable alternative to directly accessing the data.
        """
        return self.observations[sp_name][index]

    def _collect_period_samp_sizes(self, period: int) -> list:
        """Returns the sample sizes for the supplied period."""
        indecies = self.get_period_columns(period)
        samps = []
        for i in indecies:
            samps.append(self.samp_sizes[i])
        return samps

    def _collect_period_observations(self, period: int) -> dict:
        indecies = self.get_period_columns(period)
        obs_dict = {}
        for sp in self.observations:
            sp_obs = []
            for i in indecies:
                sp_obs.append(self.get_observation(sp, i))
            obs_dict[sp] = sp_obs
        return obs_dict

    def summarize_period(self, period: int) -> dict:
        """Calculates amd returms the occurance rate of each species over a provided period as a dict."""
        samps = self._collect_period_samp_sizes(period)
        obs_dict = self._collect_period_observations(period)
        summary_dict = {}
        for sp, obs in obs_dict.items():
            s = round(self.combined_average(samps, obs), 5)
            if s > 0:
                summary_dict[sp] = s
        return summary_dict

    def new_period_summary(self, period: int) -> "Summary":
        """Returns a new Summary object with data for the specified period."""
        summ = Summary()
        summ.loc_id = self.loc_id
        summ.period = period
        summ.timestamp = self.timestamp
        summ.observations = self.summarize_period(period)
        return summ

    def stash_json(self) -> None:
        """Builds a filename and calls FileManager.stash_json."""
        filename = fm.FileNameMaker.make_filename(self)
        fm.FileManager.stash_json(filename, self._to_json_string())

    def summarize_and_stash_all_periods(self) -> None:
        for p in self.PERIODS:
            summ = self.new_period_summary(p)
            summ.stash_json()

    def __repr__(self) -> str:
        return f"<Barchart object at {hex(id(self))}>"

    def __str__(self) -> str:
        pass


class Summary:
    def __init__(self) -> None:
        self.loc_id = ""
        self.period = None
        self.timestamp = ""
        self.observations = {}

    def __repr__(self) -> str:
        return f"<Summary object at {hex(id(self))}>"

    def __len__(self) -> int:
        return len(self.observations)

    def get_species(self) -> list:
        return self.observations.keys()

    def to_json_string(self) -> str:
        """Returns a json compatable string representation of this Summary."""
        out_dict = {}
        out_dict["loc_id"] = self.loc_id
        out_dict["period"] = self.period
        out_dict["timestamp"] = self.timestamp
        out_dict["observations"] = self.observations
        return str(out_dict)

    def stash_json(self) -> None:
        json_str = self.to_json_string()
        filename = fm.FileNameMaker.make_filename(self)
        fm.FileManager.stash_json(filename, json_str)

    @classmethod
    def new_from_json(cls):
        """Returns a new Summary object from a supplied JSON file."""
        # TODO: Core
        pass


if __name__ == "__main__":
    TEST_FILE = (
        Path(__file__).parent
        / "data"
        / "testing"
        / "ebird_L2741553__1900_2021_1_12_barchart.txt"
    )

    TEST_FILE_2 = (
        Path(__file__).parent
        / "data"
        / "testing"
        / "ebird_L109516__1900_2021_1_12_barchart.txt"
    )

    TEST_JSON_FILE_2 = (
        Path(__file__).parent / "data" / "barcharts" / "barchart_L109516_20210421.json"
    )

    # bc = Barchart.new_from_csv(TEST_FILE)
    bc2 = Barchart.new_from_csv(TEST_FILE_2)
    # for p in range(48):
    #    summ_dict = bc2.summarize_period(p)
    #    if summ_dict.get("Yellow-throated Warbler") == 0.00347:
    #        print(p)

    print(bc2.summarize_period(17))

    # bc_json = Barchart.new_from_json(TEST_JSON_FILE_2)
    # print(type(bc._to_json_string()))
    # bc.stash_json()
    # bc2.stash_json()
    # print(bc_csv.observations == bc_json.observations)
    # print(bc_csv.loc_id == bc_json.loc_id)
    # print(bc_csv.timestamp == bc_json.timestamp)
    # print(bc_csv.samp_sizes == bc_json.samp_sizes)
    # bc_json.summarize_and_stash_all_periods()

    # for i in range(49):
    #    print(Barchart.humanize_date_range(i))