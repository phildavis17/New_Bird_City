import calendar
import csv
import json
import math

from datetime import date
from pathlib import Path


def read_barchart_file(barchart_file) -> str:
    with open(barchart_file, "r") as in_file:
        pass


def test():
    TEST_FILE = Path(
        R"C:\Users\Phil\Desktop\Buffer\ebird_L2741553__1900_2021_1_12_barchart.txt"
    )


class Barchart:
    BC_FILE_COL_OFFSET = (
        -2
    )  # This is the offset to get the correct columns from eBird barchart files.
    BC_FILE_SAMP_SIZE_ROW = 14
    BC_FILE_OBS_START_ROW = 16

    def __init__(self) -> None:
        self.timestamp = date.today().strftime("%y%m%d")

    @classmethod
    def from_csv(cls, csv_path):
        """Returns a new Barchart object containing the data from the specified .csv file."""
        row_list = cls.read_csv_file(csv_path)
        samps = row_list[cls.BC_FILE_SAMP_SIZE_ROW][1:]
        obs = {}
        for row in cls.filter_observation_rows(row_list[cls.BC_FILE_OBS_START_ROW :]):
            sp_name = row[0]
            obs[sp_name] = row[1:]
        new_barchart = Barchart()
        new_barchart.observations = obs
        new_barchart.samp_sizes = samps
        new_barchart.loc_id = cls.loc_id_from_filename(csv_path)

    @staticmethod
    def read_csv_file(csv_path) -> list:
        """Returns a the lines of an eBird Barchart File as a list. Does no filtering."""
        with open(csv_path, "r") as in_file:
            row_list = []
            reader = csv.reader()
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
    def from_json(cls, json_path):
        pass

    @classmethod
    def get_period_columns(cls, n: int) -> list:
        cols = []
        for i in range(4):
            c = ((n + i + cls.BC_FILE_COL_OFFSET) % 48) + 1
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
        flag_strings = (" sp.", " x ", "/", "Domestic")
        for flag in flag_strings:
            if flag.lower() in species.lower():
                return False
        return True

    @staticmethod
    def clean_sp_name(sp_name: str) -> str:
        """Removes scientific name from species name cell if present."""
        # At time of writing, scientific names are all preceded by a space and an open peren.
        # If eBird changes this, this method will break.
        end_index = sp_name.find(" (")
        if end_index == -1:
            return sp_name
        return sp_name[:end_index]

    def summarize_period(self, period: int):
        pass

    def __repr__(self) -> str:
        pass

    def __str__(self) -> str:
        pass


if __name__ == "__main__":
    # for i in range(48):
    #    print(Barchart.humanize_date_range(i))

    print(Barchart.humanize_date_range(0))
    print(Barchart.get_period_columns(0))
    print(Barchart.humanize_date_range(2))
    print(Barchart.get_period_columns(2))
    print(Barchart.humanize_date_range(47))
    print(Barchart.get_period_columns(47))
