# New Bird City

A Python tool to help summarize, compare, and learn from eBird Barchart Data.

eBird allows users to download "barchart data," which contains presence/absence data for each species reported at a hotspot for 48 slices of the year. This data is incredibly useful for getting familiar with the birds you are likely to encounter in a new area, but it is presented in a way that requires an inconvenient amount of manipulation before it can be useful. This library is intended to handle that manipulation behind the scenes, and surface the information that birders need to get ready for a trip.

## Usage

### Step 1 - Download Data

The first step is to collect the barchart data for the hotspots you'd like to know more about.

- **Hotspot Data** - Download the eBird bar chart data for the hotspots you would like to summarize. This data should be for the entire year, but the span of years included is up to you. These files should be in a folder by themselves. The script will ingest any .txt file it finds in the target folder, and will not know what to do with non-ebird files. **Note:** you must rename these files. Since eBird bar chart data files do not contain the name of the hotspot from which the data was generated, the script expects that information to be present in the file name. Properly named files will begin with the name of the hotspot, followed by an underscore, like so:

    >Brooklyn Bridge Park_L1902982__...

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
