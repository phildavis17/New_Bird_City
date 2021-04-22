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


def test_file_exists_for_location():
    present_file = "L2741553"
    absent_file = "no_file"
    folder = R"D:\Douments\Code\New_Bird_City\data\testing"
    assert FileManager._file_exists_for_location(present_file, folder)
    assert not FileManager._file_exists_for_location(absent_file, folder)
