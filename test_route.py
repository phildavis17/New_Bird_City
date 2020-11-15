import pytest
import route

json_chunk_a = '''{
    "Park Names": ["Plumb Beach", "Prospect Park"], 
    "Birds": {
        "Black-bellied Whistling-Duck": {"Plumb Beach": 0.1, "Prospect Park": 0.0}, 
        "Snow Goose": {"Plumb Beach": 0.0, "Prospect Park": 0.01959},
        "Brant": {"Plumb Beach": 0.87324, "Prospect Park": 0.00178}, 
        "Canada Goose": {"Plumb Beach": 0.36821, "Prospect Park": 0.59958}}
    }'''

json_chunk_b = '''{
    "Park Names": ["Calvert Vaux Park", "Floyd Bennett Field", "Prospect Park"],
    "Birds": {
        "Black-bellied Whistling-Duck": {"Calvert Vaux Park": 0.01724, "Floyd Bennett Field": 0.0, "Prospect Park": 0.0}, 
        "Snow Goose": {"Calvert Vaux Park": 0.0, "Floyd Bennett Field": 0.0, "Prospect Park": 0.01959}, 
        "Brant": {"Calvert Vaux Park": 0.78161, "Floyd Bennett Field": 0.83756, "Prospect Park": 0.00178}, 
        "Canada Goose": {"Calvert Vaux Park": 0.54023, "Floyd Bennett Field": 0.6599, "Prospect Park": 0.59958}, 
        "Mute Swan": {"Calvert Vaux Park": 0.43678, "Floyd Bennett Field": 0.1066, "Prospect Park": 0.49392}, 
        "Wood Duck": {"Calvert Vaux Park": 0.02299, "Floyd Bennett Field": 0.09645, "Prospect Park": 0.4954}}
    }'''

@pytest.fixture
def route_fixture():
    '''Test Route creation with fixed data.'''
    test_data = route.build_master_dict(json_chunk_a)
    return route.Route(test_data, test_data['Park Names'])


def test_route_fixture(route_fixture):
    assert route_fixture is not None


def test_dunders(route_fixture):
    assert len(route_fixture) == 2

    
def test_summary_data(route_fixture):
    assert route_fixture.birds['Brant'] == 0.87347

def test_inequality():
    test_data_a = route.build_master_dict(json_chunk_a)
    test_data_b = route.build_master_dict(json_chunk_b)
    route_a = route.Route(test_data_a, test_data_a['Park Names'])
    route_b = route.Route(test_data_b, test_data_b['Park Names'])
    assert route_a != route_b

def test_compare():
    test_data_a = route.build_master_dict(json_chunk_a)
    test_data_b = route.build_master_dict(json_chunk_b)
    route_a = route.Route(test_data_a, test_data_a['Park Names'])
    route_b = route.Route(test_data_b, test_data_b['Park Names'])
    assert route_a.compare(route_b) == {'Snow Goose': 0.0, 'Canada Goose': -0.19037, 'Black-bellied Whistling-Duck': 0.08276, 'Brant': -0.09112, 'Wood Duck': -0.55455, 'Mute Swan': -0.74535}


def test_random_route():
    rand_route = route.random_route(route.MASTER_ROUTE, 3)
    assert rand_route is not None


if __name__ == "__main__":
    pytest.main()
    test_data_a = route.build_master_dict(json_chunk_a)
    test_data_b = route.build_master_dict(json_chunk_b)
    route_a = route.Route(test_data_a, test_data_a['Park Names'])
    route_b = route.Route(test_data_b, test_data_b['Park Names'])
    for bird in route_a.birds.items():
        print(bird)
    for bird in route_b.birds.items():
        print(bird)
    print(route_a.compare(route_b))
    print(route_b.compare(route_a))

    rand_route = route.random_route(route.MASTER_ROUTE, 3)
    print(rand_route.parks)

