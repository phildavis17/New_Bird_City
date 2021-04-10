import pytest
import random

from barchart import Barchart
from pathlib import Path


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


def test_get_column_bounds():
    assert len(Barchart.get_period_columns(random.randint(0, 47))) == 4
    assert min(Barchart.get_period_columns(1)) >= 0
    assert max(Barchart.get_period_columns(1)) <= 47
    assert Barchart.get_period_columns(2) == [0, 1, 2, 3]
    assert Barchart.get_period_columns(0) == [46, 47, 0, 1]


def test_humanize_period():
    # Early
    assert Barchart.humanize_date_range(1) == "Early January"
    # Mid
    assert Barchart.humanize_date_range(6) == "Mid February"
    # Late
    assert Barchart.humanize_date_range(11) == "Late March"
    # Slash
    assert Barchart.humanize_date_range(16) == "Late April/Early May"
    # Start
    assert Barchart.humanize_date_range(0) == "Late December/Early January"
    # End
    assert Barchart.humanize_date_range(47) == "Late December"


def test_clean_sp_name():
    dirty_name = 'Downy Woodpecker (<em class="sci">Dryobates pubescens</em>)'
    clean_name = "Hairy Woodpecker"
    # The doomed name must keep the '(hybrid)' part, as this is used later to indicate a bad species
    doomed_name = """Lawrence's Warbler (hybrid) (<em class="sci">Vermivora chrysoptera x cyanoptera (F2 backcross)</em>)"""
    assert Barchart.clean_sp_name(dirty_name) == "Downy Woodpecker"
    assert Barchart.clean_sp_name(clean_name) == clean_name
    assert Barchart.clean_sp_name(doomed_name) == """Lawrence's Warbler (hybrid)"""


def test_loc_from_filename():
    assert Barchart.loc_id_from_filename(TEST_FILE) == "L2741553"
    assert Barchart.loc_id_from_filename(TEST_FILE_2) == "L109516"


def test_is_good_species():
    assert Barchart.is_good_species("Snow Goose")
    # sp.
    assert not Barchart.is_good_species("dabbling duck sp.")
    # x
    assert not Barchart.is_good_species("Mallard x American Black Duck")
    # /
    assert not Barchart.is_good_species("Mallard/American Black Duck")
    # domestic
    assert not Barchart.is_good_species("Mallard (Domestic type)")
    # hybrid
    assert not Barchart.is_good_species("Lawrence's Warbler (hybrid)")


def test_filter_obs_rows():
    bad_rows = [
        [],
        ["Snow Goose", 1.0],
        ["Mallard x American Black Duck", 1.0],
        ["Lawrence's Warbler (hybrid)", 1.0],
    ]
    assert Barchart.filter_observation_rows(bad_rows) == [
        ["Snow Goose", 1.0],
    ]


def test_combined_average():
    samps = [12, 8, 9, 4]
    obs_0 = [0.0, 0.0, 0.0, 0.0]
    obs_1 = [1.0, 1.0, 1.0, 1.0]
    obs_a = [0.3333333, 0.125, 0.0, 0.25]
    obs_b = [0.5833333, 0.875, 0.7777778, 1.0]
    obs_c = [0.1666667, 0.625, 0.3333333, 0.5]

    assert Barchart.combined_average(samps, obs_0) == 0
    assert Barchart.combined_average(samps, obs_1) == 1
    assert Barchart.combined_average(samps, obs_a) == round(0.18181817, 5)
    assert Barchart.combined_average(samps, obs_b) == round(0.757575752, 5)
    assert Barchart.combined_average(samps, obs_c) == round(0.363636367, 5)


def test_new_from_csv():
    bc = Barchart.new_from_csv(TEST_FILE)
    assert bc is not None
    assert bc.loc_id == "L2741553"
    assert len(bc.observations) < 120
    assert bc.get_observation("Canada Goose", 0) == 0
    assert bc.get_observation("Double-crested Cormorant", 3) == 0.5


@pytest.mark.skip(reason="Not implimented yet.")
def test_from_json():
    pass


@pytest.mark.skip(reason="Not implimented yet.")
def test_new_to_json():
    pass


def test_summarize_period():
    bc = Barchart.new_from_csv(TEST_FILE)
    sum = bc.new_period_summary(2)
    assert sum.observations["Canada Goose"] == 0.6
    for obs in sum.observations.values():
        assert obs > 0


if __name__ == "__main__":
    pass