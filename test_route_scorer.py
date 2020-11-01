def test_route_compare():
    master_dict = parse_json(MASTER_JSON)
    park_names = master_dict['Park Names']
    #print(master_dict['Park Names'])
    route_parks_1 = random_route(3, park_names)
    route_parks_2 = random_route(3, park_names)
    A_route = build_route(master_dict, route_parks_1)
    B_route = build_route(master_dict, route_parks_2)
    print(route_compare(A_route, B_route))