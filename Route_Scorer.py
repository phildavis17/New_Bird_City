from collections import defaultdict
from decimal import *

import csv
import json
import random

MASTER_JSON = R'C:\Documents\Code\New_Bird_City\BK_May.json'
ESCAPED_KEYS = ['Park Names']

def parse_json(file_location):
    '''Reads a json file, and returns a bird dict.'''
    with open(file_location, 'r') as in_file:
        in_dict = json.load(in_file)
        in_dict['Park Names'] = tuple(in_dict['Park Names'])
    return in_dict


def random_route(count, all_parks):
    '''Generate a random route from the supplied park list.'''
    park_list = list(all_parks)
    route = []
    for i in range(count):
        random.shuffle(park_list)
        route.append(park_list.pop())
    return route


def route_birds(parks, master_dict):  # <--------------------------------------Refactor to use default dicts
    '''Returns a bird dict trimmed to the supplied parks.'''
    route_dict = {}
    #del master_dict['Park Names']
    for bird in master_dict:
        if bird in ESCAPED_KEYS: continue
        temp_dict = {}
        for park in master_dict[bird]:
            if park in parks:
                temp_dict[park] = master_dict[bird][park]
        if max(temp_dict.values()) > 0:
            route_dict[bird] = temp_dict
    route_dict['Park Names'] = tuple(sorted(parks))
    return route_dict


def calculate_probabilities(route_dict):
    '''Calculates the overall odds of seeing each birds on a specifies route.'''
    prob_dict = {}
    #del route_dict['Park Names']
    for bird in route_dict:
        if bird in ESCAPED_KEYS: continue
        prob = 1
        for obs in route_dict[bird].values():
            prob *= 1-obs
        prob_dict[bird] = round(1 - prob, 5)
    return prob_dict


def find_specialties(route_dict):
    '''Finds specialties at each park on a route.'''
    specialties = {}
    # del route_dict['Park Names']
    for bird in route_dict:
        if bird in ESCAPED_KEYS: continue
        this_bird = route_dict[bird]
        average = sum(this_bird.values())/len(this_bird.values())
        sp_dict = {}
        for park in this_bird:
            if this_bird[park] > average:
                sp_dict[park] = round(this_bird[park] - average, 5)
        specialties[bird] = sp_dict
    return specialties


def create_route_name(in_parks, all_parks):
    '''Generates a route name from the supplied set of parks'''
    rt_name = ''
    for park in all_parks:
        if park in in_parks:
            rt_name += '1'
        else:
            rt_name += '0'
    return rt_name


def build_route(master_dict, route_parks):
    '''Generates data describing a route between parks.'''
    #print('Park Names' in master_dict)

    route = {}
    all_park_names = master_dict['Park Names']
    route_dict = route_birds(route_parks, master_dict)
    route['Route Index'] = create_route_name(route_parks, all_park_names)
    route['Parks'] =  tuple(sorted(list(route_parks)))
    route['Probabilities'] = calculate_probabilities(route_dict)
    route['Specialties'] = find_specialties(route_dict)
    return route


def route_is_logged(route_file, route):
    '''determines whether a given route exists in a JOSN file of routes'''
    with open(route_file, 'r') as json_routes:
        logged_routes = json.load


def log_route_data(route_dict):
    '''Logs route information to a JSON file.'''
    pass


def route_compare(base_route, alt_route):
    '''Takes two route bird dictionaries and returns a comparison dict with the differences between routes.'''

    # Route_dict:
    #   -Index: string
    #   -Parks: tuple
    #   -Probabilites: dictionary
    #   -Specialtes: dictionary

    #base_probs = base_route['Probabilites']
    
    # fine, but not ideal!
    #   -This is creating a second copy of the info in these dicts, which is an opportunity to make a mistake!
    
    base_probs = defaultdict(float)
    for bird, probability in base_route['Probabilities'].items():
        base_probs[bird] = probability
    
    alt_probs = defaultdict(float)
    for bird, probability in alt_route['Probabilities'].items():
        alt_probs[bird] = probability

    all_birds = base_probs.keys() | alt_probs.keys()

    # It's like this because we are currently only using defailt dicts within this method.
    
    comparison = {}
    for bird in all_birds:
        comparison[bird] = round(base_probs[bird] - alt_probs[bird], 5)
    
    # to do:
    #   -sort by tax order

    return comparison   


def net_compare(comp):
    return round(sum(comp.values()), 5)


def test():
    master_dict = parse_json(MASTER_JSON)
    park_names = master_dict['Park Names']
    #print(master_dict['Park Names'])
    route_parks_1 = random_route(3, park_names)
    route_parks_2 = random_route(3, park_names)
    A_route = build_route(master_dict, route_parks_1)
    B_route = build_route(master_dict, route_parks_2)
    comp_a = route_compare(A_route, B_route)
    print(net_compare(comp_a))
    

if name == if __name__ == "__main__":
    test()



