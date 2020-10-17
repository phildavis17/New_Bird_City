import csv
import json
import random

MASTER_JSON = R'D:\Douments\Code\New_Bird_City\BK_May.json'

def parse_json(file_location):
    '''Reads a json file, and returns a bird dict.'''
    with open(file_location, 'r') as in_file:
        in_dict = json.load(in_file)
        in_dict['Park Names'] = tuple(in_dict['Park Names'])
    return in_dict
        




def random_route(count, all_parks):
    park_list = list(all_parks)
    route = []
    for i in range(count):
        random.shuffle(park_list)
        route.append(park_list.pop())
    return route




def route_birds(parks, master_dict):
    '''Returns a bird dict trimmed to the supplied parks.'''
    route_dict = {}
    del master_dict['Park Names']
    for bird in master_dict:
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
    del route_dict['Park Names']
    for bird in route_dict:
        prob = 1
        for obs in route_dict[bird].values():
            prob *= 1-obs
        prob_dict[bird] = round(1 - prob, 5)
    return prob_dict




def find_specialties(route_dict):
    '''Finds specialties at each park on a route.'''
    specialties = {}
    del route_dict['Park Names']
    for bird in route_dict:
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


def build_route(parks, all_parks):
    '''Generates data describing a route between parks.'''
    pass


def route_is_logged(route_file, route):
    '''determines whether a given route exists in a JOSN file of routes'''
    with open(route_file, 'r') as json_routes:
        logged_routes = json.load


def log_route_data(route_dict):
    '''Logs route information to a JSON file.'''
    pass

def test():
    master_dict = parse_json(MASTER_JSON)
    park_names = master_dict['Park Names']
    route_parks = random_route(5, park_names)
    rt_dict = route_birds(route_parks, master_dict)
    
    print(rt_dict['Park Names'])
    print(calculate_probabilities(rt_dict))



test()