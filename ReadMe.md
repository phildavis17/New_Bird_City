# eBird Trip Planner

A Python library to help turn eBird Bar Chart Data into a plan of action for a birding trip.

eBird allows users to download the bar chart data for any hotspot, but that data is provided in a format that can be difficult to use. The intent of this script is to summarize that data, and reformat it into something a little more useful. This script will turn several txt files with full-year barchart data into a single CSV file summarizing the observation data for every bird at every hotspot included for a specified month.

## Installation

TK

## Usage

### Step 1 - Download Data

You will need to download 2 sets of data for this script to work properly.

- **Hotspot Data** - Download the eBird bar chart data for the hotspots you would like to summarize. This data should be for the entire year, but the span of years included is up to you. These files should be in a folder by themselves. The script will ingest any .txt file it finds in the target folder, and will not know what to do with non-ebird files. **Note:** you must rename these files. Since eBird bar chart data files do not contain the name of the hotspot from which the data was generated, the script expects that information to be present in the file name. Properly named files will begin with the name of the hotspot, followed by an underscore, like so:

    >Brooklyn Bridge Park_L1902982__...

- **eBird Taxonomy** - The script sorts observation data according to the eBird taxonomy. In order for it to do so, you will need a local copy. It is available for download [here.](https://www.birds.cornell.edu/clementschecklist/download/?__hstc=60209138.7dc66638a76ffe663330f5113d61277b.1598220823146.1598928394012.1599442334159.5&__hssc=60209138.1.1599442334159&__hsfp=2418166864) **Note:** This cannot be in the same folder as the bar chart data.

### Step 2 - Configure Script

You will need to edit the script in two places to get up and running locally.

- The variable named `DATA_FOLDER` should point to the folder where you have downloaded your barchart data.
- The variable named `EBIRD_TAXONOMY_FILE` should point to the eBird Taxonomy file.

With those two set up, you should be ready to go.

### Step 3 - Run Script

The script requires two arguments:

1. The path to the CSV file to be written
2. The month you'd like to summarize, written in text

If successful, the script will report a brief summary of its activity.
