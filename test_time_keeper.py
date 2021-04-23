import pytest

from file_manager import TimeKeeper


def test_timestamp_creation():
    ts = TimeKeeper.generate_timestamp()
    assert ts is not None
    assert ts


def test_ts_to_list():
    ts = TimeKeeper.generate_timestamp()
    ts_l = TimeKeeper._ts_to_list(ts)
    assert isinstance(ts_l, list)
    assert len(ts_l) == 3
    for i in ts_l:
        assert isinstance(i, int)


def test_get_timestamp():
    ts = TimeKeeper.generate_timestamp()
    assert isinstance(ts, str)
    assert ts.isnumeric()
    assert len(ts) == 8
    try:
        int(ts)
    except ValueError:
        assert False


def test_validate_good_timestamp():
    good_timestamps = (
        "20201201",
        "21210131",
        "21210106",
    )
    for ts in good_timestamps:
        assert TimeKeeper.validate_timestamp(ts)


def test_validate_bad_timestamp():
    bad_timestamps = (
        "20200020",
        "20251320",
        "20200500",
        "20200532",
    )
    for ts in bad_timestamps:
        with pytest.raises(ValueError):
            TimeKeeper.validate_timestamp(ts)


def test_is_current():
    fresh_ts = TimeKeeper.generate_timestamp()
    assert TimeKeeper.timestamp_is_current(fresh_ts)
    very_old_ts = "19990101"
    assert not TimeKeeper.timestamp_is_current(very_old_ts)


def test_timestamp_delta():
    base_ts = "20210408"
    dif_day = "20210409"
    dif_month = "20210308"
    dif_year = "20220408"
    dif_all = "20200307"

    assert TimeKeeper._find_timestamp_delta(base_ts, dif_day) == [0, 0, 1]
    assert TimeKeeper._find_timestamp_delta(base_ts, dif_month) == [0, 1, 0]
    assert TimeKeeper._find_timestamp_delta(base_ts, dif_year) == [1, 0, 0]
    assert TimeKeeper._find_timestamp_delta(base_ts, dif_all) == [1, 1, 1]
    assert TimeKeeper._find_timestamp_delta(base_ts, base_ts) == [0, 0, 0]
