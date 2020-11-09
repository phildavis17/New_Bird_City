import pytest

test_json_chunk = '''{
    "Park Names": ["Plumb Beach", "Prospect Park"], 
    "Birds": {
        "Black-bellied Whistling-Duck": {"Plumb Beach": 0.1, "Prospect Park": 0.0}, 
        "Snow Goose": {"Plumb Beach": 0.0, "Prospect Park": 0.01959},
        "Brant": {"Plumb Beach": 0.87324, "Prospect Park": 0.00178}, 
        "Canada Goose": {"Plumb Beach": 0.36821, "Prospect Park": 0.59958}
    }}'''

import route

@pytest.fixture
def route_fixture():
    '''Test Route creation with fixed data.'''
    test_data = route.build_master_dict(test_json_chunk)
    return route.Route(test_data, test_data['Park Names'])

def test_repr(route_fixture):
    print(route_fixture)

def test_dunders(route_fixture):
    assert len(route_fixture) == 2

def test_route_fixture(route_fixture):
    assert route_fixture is not None

    
def test_summary_data(route_fixture):
    assert route_fixture.birds['Brant'] == 0.87347


if __name__ == "__main__":
    pytest.main()