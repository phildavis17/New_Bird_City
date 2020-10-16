import csv
import json

MASTER_JSON = R'C:\Documents\Code\New_Bird_City\BK_May.json'

def parse_json(file_location):
    '''Reads a json file, and returns a bird dict.'''
    with open(file_location, 'r') as in_file:
        in_dict = json.load(in_file)
        in_dict['Park Names'] = tuple(in_dict['Park Names'])
    return in_dict
        

def build_route(parks):
    '''Generates data describing a route between parks.'''
    pass


def log_route_data(route_dict):
    '''Logs route information to a JSON file.'''
    pass


def route_birds(parks, master_dict):
    '''Returns a bird dict trimmed to the supplied parks.'''
    del master_dict['Park Names']
    for bird in master_dict:
        master
    


def calculate_odds(route_dict):
    '''Calculates the overall odds of seeing each birds on a specifies route.'''
    pass


def find_specialties(route_dict):
    '''Finds specialties at each park on a route.'''
    pass


def create_route_name(in_parks, all_parks):
    '''Generates a route name from the supplied set of parks'''
    rt_name = ''
    for park in all_parks:
        if park in in_parks:
            rt_name += '1'
        else:
            rt_name += '0'
    return rt_name



def test():
    parse_json(MASTER_JSON)


test()