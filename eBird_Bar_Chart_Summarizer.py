"""Toos for summarizing Bar Chart Data txt files downloaded from eBird."""

from pathlib import Path

import argparse
import csv
import json

# Isolation -- use different libraries for different projects
# Reproducibility -- never accidentally change the code you are running
# Intent -- write down the libraries your project needs

# python -m venv --help
# python -m venv env
# in vscode, start the command palette Ctrl+Shift+P
# find the python: select interpreter command

# pip-compile
# pyenv
# pyenv-win
# chocolaty


def combined_average(samp_size, presence):
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
    if not len(samp_size) == len(presence):
        raise IndexError("Lists must have the same length.")
    total_num_present = 0
    data = zip(samp_size, presence)
    for pair in data:
        total_num_present += round(pair[0] * pair[1])
    return total_num_present / sum(samp_size)


def generate_species_list(dicts):
    """Returns a cumulative list of the unique keys in the provided dicts."""
    sp_list = []
    for dic in dicts:
        for species in dic.keys():
            if species not in sp_list:
                sp_list.append(species)
    return sp_list


def make_period_bounds(period):
    """Returns the column numbers that correspond to the chosen period in an eBird barchart data file."""
    month_index = {
        "jan": 1,
        "feb": 5,
        "mar": 9,
        "apr": 13,
        "may": 17,
        "jun": 21,
        "jul": 25,
        "aug": 29,
        "sep": 33,
        "oct": 37,
        "nov": 41,
        "dec": 45,
    }
    return month_index[period], month_index[period] + 4


def summarize_barchart_file(file, period):
    """Summarizes occurance data in an eBird bar chart data txt file over a specified period.

    Args:
        file: The path to the file to summarize.
        period: A string indicating the period to summarize.

    Returns:
        A dict summarizing occurance data over the specified period
    """
    p_start, p_end = make_period_bounds(period)
    samp_size = []
    bird_dict = {}
    with open(file) as tsv_file:
        hotspot_file = csv.reader(tsv_file, dialect="excel-tab")
        for row_num, row in enumerate(hotspot_file):
            if (
                row_num == 14
            ):  # Sample size information is on the 14th line of eBird bar chard data
                samp_size = list(map(float, row[p_start:p_end]))
            if row_num >= 16 and len(row):  # Occurance data starts on line 16
                sp_name = (
                    row[0].split("(<")[0].strip()
                )  # Strip HTML tag from species name if present
                raw_bird_data = list(map(float, row[p_start:p_end]))
                bird_summary = combined_average(samp_size, raw_bird_data)
                bird_dict[sp_name] = bird_summary
    return bird_dict


def summarize_barchart_files(files, period):
    """Summarizes multiple eBird bar char data files.

    Extracts hotspot names from the names of supplied files, splitting at the first underscore. Requires filenames to take the form "Hotspot Name_..."
    Args:
        files: A list of files to be summarized
        period:

    Returns: A dict of dicts in the following format
        {'Hotspot 1': {'Bird1': 0.1, 'Bird2': 0.4,...}, 'Hotspot 2': {'Bird1': 0.3, 'Bird2': 0.2,...},...}
    """
    master_dict = {}
    for file in files:
        hotspot_name = str(file.stem).split("_")[0].strip()
        master_dict[hotspot_name] = filter_bird_dict(
            summarize_barchart_file(file, period)
        )
    return master_dict


def is_good_species(species):
    """Tests a supplied species name for substrings that indicate it is a sub-species level taxon."""
    flag_strings = [" sp.", " x ", "/", "Domestic"]
    for flag in flag_strings:
        if flag.lower() in species.lower():
            return False
    return True


def filter_bird_dict(b_dict, r_digits=5):
    """Filters keys of supplied dict.

    Removes sub-species level taxons, birds that were not seen in the specified period,
    and rounds value to a specified length.
    """
    filtered_dict = {}
    for bird in b_dict:
        if not b_dict[bird] == 0.0 and is_good_species(bird):
            filtered_dict[bird] = round(b_dict[bird], r_digits)
    return filtered_dict


def species_dict_from_hotspot_dict(sp_list, m_dict):
    """Converts a hotspot oriented dict to a species oriented dict.

    Returned dict will be of following format:
        {'Bird1: {'Hotspot1': 0.23, 'Hotspot2': 0.42,...}, 'Bird2': {'Hotspot1': 0.84, 'Hotspot2': 0.77,...},...}
    """
    master_sp_dict = {}
    for species in sp_list:
        sp_dict = {}
        for hotspot in m_dict.keys():
            if species in m_dict[hotspot].keys():
                sp_dict[hotspot] = m_dict[hotspot][species]
            else:
                sp_dict[hotspot] = 0.0
        master_sp_dict[species] = sp_dict
    return master_sp_dict


def write_csv_file(file_location, sp_data):
    """Records supplied species oriented dict to a CSV at the supplied location."""
    hotspot_names = []
    for bird in sp_data.values():
        for hotspot in bird.keys():
            if not hotspot in hotspot_names:
                hotspot_names.append(hotspot)
    hotspot_names.insert(0, "Species")

    with open(file_location, "w", newline="") as out_file:
        writer = csv.writer(out_file, hotspot_names)
        writer.writerow(hotspot_names)
        for bird_dict in sp_data:
            p_vals = list(sp_data[bird_dict].values())
            p_vals.insert(0, bird_dict)
            writer.writerow(p_vals)


def write_json_file(file_location, sp_data):
    """Records supplied species oriented dict to a JSON file at the supplied location"""
    data_dict = {}
    hotspot_names = []
    for bird in sp_data.values():
        for hotspot in bird.keys():
            if not hotspot in hotspot_names:
                hotspot_names.append(hotspot)
        break
    hotspot_names = sorted(hotspot_names)

    bird_dict = {}
    for bird in sp_data:
        bird_dict[bird] = sp_data[bird]

    data_dict["Hotspot Names"] = hotspot_names
    data_dict["Birds"] = bird_dict

    with open(file_location, "w") as out_file:
        json.dump(data_dict, out_file)


def sort_species_dict(sp_dict):
    """Sorts a supplied species oriented dict according to an eBird taxonomy file"""
    EBIRD_TAXONOMY_FILE = R"D:\Douments\Code\New Bird City\General Info\eBird_Taxonomy_v2019.csv"  # Change location of eBird Taxonomy file here
    sorted_sp_dict = {}
    with open(EBIRD_TAXONOMY_FILE) as taxonomy:
        tax_reader = csv.reader(taxonomy)
        for row in tax_reader:
            this_sp = row[3]
            if this_sp in sp_dict.keys():
                sorted_sp_dict[this_sp] = sp_dict[this_sp]
    return sorted_sp_dict


def main():
    """Summarizes the bar chart data files in a folder for a specified month, and writes a CSV to a specified location."""
    DATA_FOLDER = Path(
        R"D:\Douments\Code\New Bird City\Whole Year Data"
    )  # Change data location here.

    parser = argparse.ArgumentParser(
        description="Read eBird Bar Chart Data txt files, and create a CSV file summarizing occurance data over a specified month."
    )
    parser.add_argument(
        "ouput_location", type=str, help="The output location for the created CSV file."
    )
    parser.add_argument("month", type=str, help="The month to summarize.")

    args = parser.parse_args()
    out_file_path = Path(args.ouput_location)
    month = args.month.lower()[:3]

    file_name_list = DATA_FOLDER.glob("*.txt")
    file_list = []
    for file in file_name_list:
        file_list.append(DATA_FOLDER / file)

    master_hotspot_dict = summarize_barchart_files(file_list, month)
    species_list = generate_species_list(master_hotspot_dict.values())

    master_species_dict = species_dict_from_hotspot_dict(
        species_list, master_hotspot_dict
    )

    sorted_master_dict = sort_species_dict(master_species_dict)

    # write_csv_file(out_file_path, sorted_master_dict)
    write_json_file(out_file_path, sorted_master_dict)
    print(
        f"Summary file written for {len(species_list)} species and {len(file_list)} hotspots."
    )


def test():
    # Testing Supplies
    TEST_FILE = Path(
        R"D:\Douments\Code\New Bird City\Test Data\Greenwood Cemetery_L285884__2010_2020_1_12_barchart.txt"
    )
    TEST_DATA_FOLDER = Path(R"D:\Douments\Code\New Bird City\Test Data")
    TEST_OUT_FILE = "eBird_test.csv"
    TEST_SAMP_SIZE = [266, 235, 209, 112]
    TEST_PRES_DATA = [0.725564, 0.731915, 0.698565, 0.660714]

    file_name_list = TEST_DATA_FOLDER.glob("*.txt")
    file_list = []
    for file in file_name_list:
        file_list.append(TEST_DATA_FOLDER / file)

    m_dict = summarize_barchart_files(file_list, "jan")
    sp_list = generate_species_list(m_dict.values())
    master_sp_dict = species_dict_from_hotspot_dict(sp_list, m_dict)

    write_csv_file(TEST_OUT_FILE, master_sp_dict)


if __name__ == "__main__":
    # import sys
    # print(sys.path)
    main()