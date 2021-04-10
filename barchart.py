import calendar
import csv
import json
import math

from file_manager import FileManager
from pathlib import Path


class Barchart:
    BC_FILE_COL_OFFSET = (
        -2
    )  # This is the offset to get the correct columns from eBird barchart files.
    BC_FILE_SAMP_SIZE_ROW = 14
    BC_FILE_OBS_START_ROW = 16

    def __init__(self) -> None:
        self.timestamp = FileManager.get_timestamp()

    @staticmethod
    def new_from_csv(csv_path):
        """Returns a new Barchart object containing the data from the specified .csv file."""
        new_barchart = Barchart()
        new_barchart.ingest_csv(csv_path)
        return new_barchart

    def ingest_csv(self, csv_path: Path) -> None:
        """Populates Barchart data from a provided eBird barchart file."""
        row_list = self._read_csv_file(csv_path)
        samps = [int(float(x)) for x in row_list[self.BC_FILE_SAMP_SIZE_ROW][1:] if x]
        obs = {}
        for row in self.filter_observation_rows(row_list[self.BC_FILE_OBS_START_ROW :]):
            sp_name = self.clean_sp_name(row[0])
            obs[sp_name] = [float(x) for x in row[1:] if x]
        self.loc_id = self.loc_id_from_filename(csv_path)
        self.samp_sizes = samps
        self.observations = obs

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
    def loc_id_from_filename(csv_path: Path) -> str:
        """Returns the location ID of a hotspot from an eBird bar chart file name. Assumes file has not been renamed."""
        return csv_path.stem.split("_")[1]

    @classmethod
    def new_from_json(cls, json_path: Path):
        # TODO: Core
        pass

    def ingest_json(self, json_path: Path):
        # TODO: Core
        pass

    @staticmethod
    def read_json_file(json_path: Path):
        # TODO: Core
        pass

    def _to_json_string(self) -> str:
        """Creates a json compatable string representation of this Barchart object."""
        out_dict = {}
        out_dict["loc_id"] = self.loc_id
        out_dict["timestamp"] = self.timestamp
        out_dict["samp_sizes"] = self.samp_sizes
        out_dict["observations"] = self.observations
        return json.dumps(out_dict)

    @staticmethod
    def stash_json(out_path: Path) -> None:
        # TODO: Core
        # This should check to make sure there is not an existing version of this hotspot in the folder
        pass

    @classmethod
    def get_period_columns(cls, n: int) -> list:
        cols = []
        for i in range(4):
            c = (n + i + cls.BC_FILE_COL_OFFSET) % 48
            cols.append(c)
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
        # At time of writing, scientific names are all preceded by a space and an open peren.
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
        return round(total_num_present / sum(samp_sizes), 5)

    def get_observation(self, sp_name: str, index: int) -> float:
        return self.observations[sp_name][index]

    def _collect_period_samp_sizes(self, period: int) -> list:
        """Returns the sample sizes for the supplied period"""
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
        samps = self._collect_period_samp_sizes(period)
        obs_dict = self._collect_period_observations(period)
        summary_dict = {}
        for sp, obs in obs_dict.items():
            s = round(self.combined_average(samps, obs), 5)
            if s > 0:
                summary_dict[sp] = s
        return summary_dict

    def new_period_summary(self, period: int):
        # TODO: Core
        summ = Summary()
        summ.loc_id = self.loc_id
        summ.period = period
        summ.timestamp = self.timestamp
        summ.observations = self.summarize_period(period)
        return summ

    def _make_filename(self):
        filename = f"{self.loc_id}_barchart_{self.timestamp}"
        return filename

    def stash_json(self):
        FileManager.stash_barcart_json(self._make_filename(), self._to_json_string())

    def summarize_all_periods_to_folder(self, out_folder: Path) -> None:
        # TODO: Core
        pass

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

    def make_filename(self) -> str:
        filename = f"{self.loc_id}_{self.period}_summary_{self.timestamp}"
        return filename

    def stash_json(self) -> None:
        json_str = self.to_json_string()
        filename = self.make_filename()
        # FileManager.stash_json()


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

    bc = Barchart.new_from_csv(TEST_FILE)
    bc2 = Barchart.new_from_csv(TEST_FILE_2)
    # print(type(bc._to_json_string()))
    bc.stash_json()
    bc2.stash_json()
