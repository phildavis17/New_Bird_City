import csv
from pathlib import Path

TAXONOMY_PATH = Path(__file__).parent/"data"/"eBird_Taxonomy_v2019.csv"

big_set = set()

with open(TAXONOMY_PATH, 'r') as tax_file:
    reader = csv.reader(tax_file)
    for line in reader:
        if not line[1] == "species": continue
        if int(line[0]) in big_set:
            print(line)
        big_set.add(int(line[0]))
    
print(len(big_set))