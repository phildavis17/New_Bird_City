from collections import defaultdict
from decimal import *

import csv
import hashlib
import json
import random


MASTER_JSON = R'D:\Douments\Code\New_Bird_City\BK_May_2.json'  # Desktop Version
#MASTER_JSON = R'C:\Documents\Code\New_Bird_City\BK_May_2.json'  # Laptop Version

def parse_json(file_location):
    '''Reads a json file, and returns a bird dict.'''
    with open(file_location, 'r') as in_file:
        in_dict = json.load(in_file)
        in_dict['Park Names'] = tuple(in_dict['Park Names'])
    return in_dict


def random_route(master_dict, num):
    '''Creates a random route from the supplied parks.'''
    pass


class Route:
    '''A class to handle routes between parks.'''
    
    parks = ()
    index = ''
    birds = {}
    specialties = {}
    score = 0
    total_species = 0
    master_hash = ''

    def __init__(self, master_dict, park_names):
        '''It's an init funtion. It populates variables.'''
        self.parks = tuple(sorted(park_names))
        self.index = self.generate_index(master_dict['Park Names'])
        self.master_hash = 
        self.birds = self.build_route_dict(master_dict['Birds'])
        self.specialties = self.find_specialties(master_dict['Birds'])
        self.score = sum(self.birds.values())
        self.total_species = len(self.birds)

    def __len__(self):
        return len(self.parks)

    def __repr__(self):
        rep_str = 'A Route objects with parks: {}'
        return rep_str.format(self.parks)

    def __str__(self):
        pass
        s = 'A Route including '

    def __eq__(self, other_route):
        if other_route.index == self.index and other_route.master_hash == self.master_hash:
            return True
        return False
        
    def generate_index(self, all_parks):
        '''Generates a route name from the supplied set of parks'''
        rt_name = ''
        for park in all_parks:
            if park in self.parks:  # We can iterate through all parks here because they are already sorted.
                rt_name += '1'
            else:
                rt_name += '0'
        return rt_name

    def generate_master_hash(self, master_dict):
        '''Creates a hash from the master dict, for use in determining route equality.'''
        hasher = hashlib.sha256()
        hasher.update(str(master_dict).encode)
        return hasher.hexdigest()

    def build_route_dict(self, master_dict):
        '''Creates a defaultdict with projected odds for birds across the whole route.'''
        route_dict = defaultdict(float)
        for bird in master_dict:
            temp_dict = {}
            for park in master_dict[bird]:
                if park in self.parks:
                    temp_dict[park] = master_dict[bird][park]
            if max(temp_dict.values()) > 0:
                route_dict[bird] = temp_dict
        return route_dict        

    def find_specialties(self, master_dict):
        '''Finds parks where the odds of seeing a bird are above the average odds on that route.'''
        specialties = {}
        for bird in self.birds:
            this_bird = self.birds[bird]
            average = sum(this_bird.values())/len(this_bird.values())
            sp_dict = {}
            for park in this_bird:
                if this_bird[park] > average:
                    sp_dict[park] = round(this_bird[park] - average, 5)
            specialties[bird] = sp_dict
        return specialties

    def compare(self, alt_route):
        '''Generates a dictionary containing the difference in odds between routes for each bird on those routes.'''
        pass




