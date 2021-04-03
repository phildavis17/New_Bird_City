import pytest
import random

from barchart import Barchart


def test_get_column_bounds():
    # generate a random number 0 - 47
    # len == 4
    # somehow that they are consecutive
    assert len(Barchart.get_period_columns(random.randint(0, 47))) == 4
    assert min(Barchart.get_period_columns(1)) >= 1
    assert max(Barchart.get_period_columns(1)) <= 48
    assert Barchart.get_period_columns(2) == [1, 2, 3, 4]
    assert Barchart.get_period_columns(0) == [47, 48, 1, 2]


def test_humanize_period():
    # Early
    assert Barchart.humanize_date_range(1) == "Early January"
    # Mid
    assert Barchart.humanize_date_range(6) == "Mid February"
    # Late
    assert Barchart.humanize_date_range(11) == "Late March"
    # Slash
    assert Barchart.humanize_date_range(16) == "Late April/Early May"

    # 48 (end)
    # Early
    # Mid
    # Late
    # Slash
    #
    pass


def test_clean_sp_name():
    dirty_name = 'Downy Woodpecker (<em class="sci">Dryobates pubescens</em>)'
    clean_name = "Hairy Woodpecker"
    assert Barchart.clean_sp_name(dirty_name) == "Downy Woodpecker"
    assert Barchart.clean_sp_name(clean_name) == clean_name


@pytest.mark.skip(reason="Not implimented yet.")
def test_from_csv():
    pass


@pytest.mark.skip(reason="Not implimented yet.")
def test_from_json():
    pass


@pytest.mark.skip(reason="Not implimented yet.")
def test_to_json():
    pass


@pytest.mark.skip(reason="Not implimented yet.")
def test_summarize_period():
    pass


if __name__ == "__main__":
    pass