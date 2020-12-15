import flask
import pytest
import trip

json_chunk_a = '''{
    "Hotspot Names": ["Plumb Beach", "Prospect Park"], 
    "Birds": {
        "Black-bellied Whistling-Duck": {"Plumb Beach": 0.1, "Prospect Park": 0.0}, 
        "Snow Goose": {"Plumb Beach": 0.0, "Prospect Park": 0.01959},
        "Brant": {"Plumb Beach": 0.87324, "Prospect Park": 0.00178}, 
        "Canada Goose": {"Plumb Beach": 0.36821, "Prospect Park": 0.59958}}
    }'''

json_chunk_b = '''{
    "Hotspot Names": ["Calvert Vaux Park", "Floyd Bennett Field", "Prospect Park"],
    "Birds": {
        "Black-bellied Whistling-Duck": {"Calvert Vaux Park": 0.01724, "Floyd Bennett Field": 0.0, "Prospect Park": 0.0}, 
        "Snow Goose": {"Calvert Vaux Park": 0.0, "Floyd Bennett Field": 0.0, "Prospect Park": 0.01959}, 
        "Brant": {"Calvert Vaux Park": 0.78161, "Floyd Bennett Field": 0.83756, "Prospect Park": 0.00178}, 
        "Canada Goose": {"Calvert Vaux Park": 0.54023, "Floyd Bennett Field": 0.6599, "Prospect Park": 0.59958}, 
        "Mute Swan": {"Calvert Vaux Park": 0.43678, "Floyd Bennett Field": 0.1066, "Prospect Park": 0.49392}, 
        "Wood Duck": {"Calvert Vaux Park": 0.02299, "Floyd Bennett Field": 0.09645, "Prospect Park": 0.4954}}
    }'''

@pytest.fixture
def _fixture():
    '''Test Trip creation with fixed data.'''
    test_data = trip.build_master_dict(json_chunk_a)
    return trip.Trip(test_data, test_data['Hotspot Names'])


def test_trip_fixture(trip_fixture):
    assert trip_fixture is not None


def test_dunders(trip_fixture):
    assert len(trip_fixture) == 2

    
def test_summary_data(trip_fixture):
    assert trip_fixture.birds['Brant'] == 0.87347

def test_inequality():
    test_data_a = trip.build_master_dict(json_chunk_a)
    test_data_b = trip.build_master_dict(json_chunk_b)
    trip_a = trip.Trip(test_data_a, test_data_a['Hotspot Names'])
    trip_b = trip.Trip(test_data_b, test_data_b['Hotspot Names'])
    assert trip_a != trip_b

def test_compare():
    test_data_a = trip.build_master_dict(json_chunk_a)
    test_data_b = trip.build_master_dict(json_chunk_b)
    trip_a = trip.Trip(test_data_a, test_data_a['Hotspot Names'])
    trip_b = trip.Trip(test_data_b, test_data_b['Hotspot Names'])
    assert trip_a.compare(trip_b) == {'Snow Goose': 0.0, 'Canada Goose': -0.19037, 'Black-bellied Whistling-Duck': 0.08276, 'Brant': -0.09112, 'Wood Duck': -0.55455, 'Mute Swan': -0.74535}


def test_random_trip():
    rand_trip = trip.random_trip(trip.MASTER_ROUTE, 3)
    assert rand_trip is not None

def test_specialties():
    pass

if __name__ == "__main__":
    pytest.main()
    test_data_a = trip.build_master_dict(json_chunk_a)
    test_data_b = trip.build_master_dict(json_chunk_b)
    trip_a = trip.Trip(test_data_a, test_data_a['Hotspot Names'])
    trip_b = trip.Trip(test_data_b, test_data_b['Hotspot Names'])
    for bird in trip_a.birds.items():
        print(bird)
    for bird in trip_b.birds.items():
        print(bird)
    print(trip_a.compare(trip_b))
    print(trip_b.compare(trip_a))

    rand_trip = trip.random_trip(trip.MASTER_ROUTE, 3)
    print(rand_trip.hotspots)

