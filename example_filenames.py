# COMPONENTS: (type, loc_id, title, period, timestamp, hs_bv)


# Formats:
# - barchart : ("type", "loc_id", "timestamp"),
# - summary : ("type", "loc_id", "period", "timestamp"),
# - analysis : ("type", "title", "period"),
# - trip : ("type", "title", "period", "hs_bv"),

# Types of problems:
# - out of order
# - double extension
# - bad extension????????
# - no filename
# - no seperators
# - bad seperator
# - giberish


GOOD_FILENAMES = [
    "barchart_L109516_20210409.json",
    "barchart_L109516_20210409",
    "summary_L109516_1_20210409.json",
    "summary_L109516_1_20210409",
    "analysis_Cool Trip to NYC_24.json",
    "analysis_Cool Trip to NYC_24",
    "trip_Cool Trip to NYC_24_0100110.json",
    "trip_Cool Trip to NYC_24_0100110",
]

BAD_FILENAMES = [
    "",
    "mmmmmmmmmmmmmmmmmm",
    "barchar_L109516_20210409",
    "barchart_L109516_20210449.json",
    "barchart_L109516_20212409.json",
    "barchart_L109516_212409.json",
    "L109516_barchart_20210409.json",
    "barchart_L109516_20210409.json.json",
    "barchartL10951620210409.json",
    "barchart-L109516-20210409.json",
]
