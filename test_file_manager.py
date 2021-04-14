from pathlib import Path
import pytest

from file_manager import FileManager

TESTING_FOLDER = Path(__file__).parent / "data" / "testing"


def test_timestamp():
    # Timestamp format should be "yyyymmdd"
    ts = FileManager.get_timestamp()
    assert type(ts) == str
    assert len(ts) == 8
    try:
        int(ts)
    except Exception as exc:
        assert False, f"timestamp conversion to int raised exception: {exc}"


def test_timestamp_to_list():
    ts = "20210408"
    assert FileManager._ts_to_list(ts) == [2021, 4, 8]


def test_timestamp_delta():
    base_ts = "20210408"
    dif_day = "20210409"
    dif_month = "20210308"
    dif_year = "20220408"
    dif_all = "20200307"

    assert FileManager._find_timestamp_delta(base_ts, dif_day) == [0, 0, 1]
    assert FileManager._find_timestamp_delta(base_ts, dif_month) == [0, 1, 0]
    assert FileManager._find_timestamp_delta(base_ts, dif_year) == [1, 0, 0]
    assert FileManager._find_timestamp_delta(base_ts, dif_all) == [1, 1, 1]
    assert FileManager._find_timestamp_delta(base_ts, base_ts) == [0, 0, 0]


def test_file_exists_for_location():
    present_file = "L2741553"
    absent_file = "no_file"
    folder = R"D:\Douments\Code\New_Bird_City\data\testing"
    assert FileManager._file_exists_for_location(present_file, folder)
    assert not FileManager._file_exists_for_location(absent_file, folder)


def test_timestamp_from_filename():
    fn = "L2741553_2_summary_210408.json"
    assert FileManager._ts_from_filename(fn) == "210408"


def test_loc_id_from_filename():
    fn = "L2741553_2_summary_210408.json"
    assert FileManager._loc_id_from_filename(fn) == "L2741553"
