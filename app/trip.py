from collections import defaultdict
from decimal import *

import csv
import hashlib
import json
import random


MASTER_JSON = R'D:\Douments\Code\New_Bird_City\BK_May_3.json'  # Desktop Version
# MASTER_JSON = R'C:\Documents\Code\New_Bird_City\BK_May_3.json'  # Laptop Version


def parse_json(file_location):
    '''Reads a json file, and returns a bird dict.'''
    with open(file_location, 'r') as in_file:
        in_dict = json.load(in_file)
    return in_dict


def build_master_dict(data_string):
    '''Turn a string into a properly formatted dict for analysis.'''
    in_dict = json.loads(data_string)
    in_dict['Hotspot Names'] = tuple(in_dict['Hotspot Names'])
    return in_dict


def random_trip(master_dict, num):
    '''Creates a random trip from the supplied hotspots.'''
    hotspot_list = list(master_dict['Hotspot Names'])
    trip_hotspots = []
    for i in range(num):
        random.shuffle(hotspot_list)
        trip_hotspots.append(hotspot_list.pop())    
    return Trip(master_dict, trip_hotspots)


def trip_from_index(master_dict, index):
    '''Creates a trip from a given index'''
    trip_hotspots = []
    if len(index) != len(master_dict['Hotspot Names']):
        raise IndexError('Index does not match hotspots')
    for i, bit in enumerate(index):
        if index[i] == '1':
            trip_hotspots.append(master_dict['Hotspot Names'][i])
    return Trip(master_dict, trip_hotspots)

def build_master_trip(master_dict):
    '''Creates a Trip object including all parks'''
    return Trip(master_dict, master_dict['Hotspot Names'])

class Trip:
    '''A class to handle trips between hotspots.'''
    
    def __init__(self, master_dict, hotspot_names):
        '''It's an init funtion. It populates variables.'''
        self.hotspots = tuple(sorted(hotspot_names))
        self.index = self._generate_index(master_dict['Hotspot Names'])
        self.context_hash = self._generate_context_hash(master_dict)
        self.birds = self._build_trip_dict(master_dict['Birds'])
        self.specialties = self._find_specialties(master_dict['Birds'])
        self.score = round(sum(self.birds.values()), 5)
        self.total_species = len(self.birds)

    def __len__(self):
        return len(self.hotspots)

    def __repr__(self):
        rep_str = 'A Trip object for hotspots: {}'
        return rep_str.format(self.hotspots)

    def __eq__(self, other_trip):
        if other_trip.index == self.index and other_trip.context_hash == self.context_hash:
            return True
        return False
        
    def _generate_index(self, all_hotspots):
        '''Generates a trip name from the supplied set of hotspots'''
        rt_name = ''
        for hotspot in all_hotspots:
            if hotspot in self.hotspots:  # We can iterate through all hotspots here because they are already sorted.
                rt_name += '1'
            else:
                rt_name += '0'
        return rt_name

    def _generate_context_hash(self, master_dict):
        '''Creates a hash from the master dict, for use in determining trip equality.'''
        hasher = hashlib.sha256()
        hasher.update(str(master_dict).encode())
        return hasher.hexdigest()
    
    def _build_trip_dict(self, master_dict):
        '''Creates a defaultdict with projected odds for birds across the whole trip.'''
        trip_dict = defaultdict(float)
        for bird in master_dict:
            prob = 1
            for hotspot in master_dict[bird]:
                if hotspot in self.hotspots:
                    prob *= 1 - master_dict[bird][hotspot]
            if prob != 1:
                trip_dict[bird] = round(1 - prob, 5)
        return trip_dict

    def _find_specialties(self, master_dict):
        '''Finds hotspots where the odds of seeing a bird are above the average odds on that trip.'''
        specialties = {}
        for bird in self.birds:
            this_bird = {}
            for hotspot in master_dict[bird]:
                if hotspot in self.hotspots:
                    this_bird[hotspot] = master_dict[bird][hotspot]

            average = sum(this_bird.values())/len(this_bird.values())
            specialties_dict = {}
            for hotspot in this_bird:
                if this_bird[hotspot] > average:
                    specialties_dict[hotspot] = round(this_bird[hotspot] - average, 5)
            specialties[bird] = specialties_dict
        return specialties

    def compare(self, alt_trip):
        '''Generates a dictionary containing the difference in odds between trips for each bird on those trips.'''
        all_birds = self.birds.keys() | alt_trip.birds.keys()
        comparison = {}
        for bird in all_birds:
            comparison[bird] = round(self.birds[bird] - alt_trip.birds[bird], 5)
        return comparison

    def compare_verbose(self, alt_trip):
        pass


with open(MASTER_JSON, 'r') as in_file:
        MASTER_TRIP = build_master_dict(in_file.read())


def test():
    master_data = parse_json(MASTER_JSON)
    #print(master_data)
    test_trip = random_trip(master_data, 3)
    print(test_trip.hotspots)
    print(test_trip.score)
    print(test_trip.total_species)
    

if __name__ == "__main__":
    test()

