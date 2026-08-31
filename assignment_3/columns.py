names_of_columns = [
    # Size of the paddy field
    ("hectares", "Hectares"),
    # Agricultural block/location where the crop is grown
    ("agriblock", "Agriblock"),
    # Paddy/rice variety planted
    ("variety", "Variety"),
    # Type of soil
    ("soil_type", "Soil Types"),
    # Quantity of seed used
    ("seed_rate", "Seedrate (in Kg)"),
    # Land-preparation/main-field input quantity
    ("lp_mainfield", "Land Preparation, Main-field (in Tonnes)"),
    # Nursery cultivation method (wet or dry)
    ("nursery", "Nursery"),
    # Area used for the nursery
    ("nursery_area", "Nursery area (Cents)"),
    # Land-preparation/input quantity associated with nursery area
    ("lp_nursery_area", "Land Preparation, Nursery area (in Tonnes)"),
    # DAP fertilizer application around 20 days after planting
    ("dap_d20", "DAP, in 20 days"),
    # Thiobencarb herbicide applied around 28 days
    ("weed_d28_thiobencarb", "Weed, in 28 days, thiobencarb"),
    # Urea application around 40 days
    ("urea_d40", "Urea, in 40 days"),
    # Potassium fertilizer application around 50 days
    ("potash_d50", "Potassh, in 50 days"),
    # Micronutrient application around 70 days
    ("micronutrients_d70", "Micronutrients, in 70 days"),
    # Pesticide applied around 60 days
    ("pesticide_d60", "Pesticide, 60 Day (in ml)"),
    # Rainfall during days X–Y
    ("rainfall_d1_d30", "Rainfall in days 01 to 30 (in mm)"),
    # Irrigation during days X–Y
    ("irrigation_d1_d30", "Irrigation in days 01 to 30 (in mm)"),
    ("rainfall_d30_d50", "Rainfall in days 30 to 50 (in mm)"),
    ("irrigation_d30_d50", "Irrigation in days 30 to 50 (in mm)"),
    ("rainfall_d51_d70", "Rainfall in days 51 to 70 (in mm)"),
    ("irrigation_d51_d70", "Irrigation in days 51 to 70 (in mm)"),
    ("rainfall_d71_d105", "Rainfall in days 71 to 105 (in mm)"),
    ("irrigation_d71_d105", "Irrigation in days 71 to 105 (in mm)"),
    # Minimum temperature in days X–Y
    ("min_temp_d1_d30", "Minimum temperature in days 01 to 30 (in Celsius)"),
    # Maximum temperature in days X–Y
    ("max_temp_d1_d30", "Maximum temperature in days 01 to 30 (in Celsius)"),
    ("min_temp_d31_d60", "Minimum temperature in days 31 to 60 (in Celsius)"),
    ("max_temp_d31_d60", "Maximum temperature in days 31 to 60 (in Celsius)"),
    ("min_temp_d61_d90", "Minimum temperature in days 61 to 90 (in Celsius)"),
    ("max_temp_d61_d90", "Maximum temperature in days 61 to 90 (in Celsius)"),
    ("min_temp_d91_d120", "Minimum temperature in days 91 to 120 (in Celsius)"),
    ("max_temp_d91_d120", "Maximum temperature in days 91 to 120 (in Celsius)"),
    # Instantaneous Wind Speed during days X–Y
    ("wind_speed_d1_d30", "Instantaneous Wind Speed in days 01 to 30 (in Knots)"),
    ("wind_speed_d31_d60", "Instantaneous Wind Speed in days 31 to 60 (in Knots)"),
    ("wind_speed_d61_d90", "Instantaneous Wind Speed in days 61 to 90 (in Knots)"),
    ("wind_speed_d91_d120", "Instantaneous Wind Speed in days 91 to 120 (in Knots)"),
    # Recorded Wind Direction during days X–Y
    ("wind_direction_d1_d30", "Wind Direction in days 01 to 30"),
    ("wind_direction_d31_d60", "Wind Direction in days 31 to 60"),
    ("wind_direction_d61_d90", "Wind Direction in days 61 to 90"),
    ("wind_direction_d91_d120", "Wind Direction in days 91 to 120"),
    # Relative Humidity during days X–Y
    ("relative_humidity_d1_d30", "Relative Humidity in days 01 to 30 (%)"),
    ("relative_humidity_d31_d60", "Relative Humidity in days 31 to 60 (%)"),
    ("relative_humidity_d61_d90", "Relative Humidity in days 61 to 90 (%)"),
    ("relative_humidity_d91_d120", "Relative Humidity in days 91 to 120 (%)"),
    # Agricultural residue present
    ("trash", "Trash (in bundles)"),
    # Paddy produced from the field
    ("paddy_yield", "Paddy yield (in Kg)"),
]


target_columns = ["paddy_yield_per_hectare", "trash_per_hectare"]


categorical_columns = [
    "agriblock",
    "variety",
    "soil_type",
    "nursery",
    "wind_direction_d1_d30",
    "wind_direction_d31_d60",
    "wind_direction_d61_d90",
    "wind_direction_d91_d120",
]


numerical_columns = [
    "hectares",
    "seed_rate",
    "lp_mainfield",
    "nursery_area",
    "lp_nursery_area",
    "dap_d20",
    "weed_d28_thiobencarb",
    "urea_d40",
    "potash_d50",
    "micronutrients_d70",
    "pesticide_d60",
    "rainfall_d1_d30",
    "irrigation_d1_d30",
    "rainfall_d30_d50",
    "irrigation_d30_d50",
    "rainfall_d51_d70",
    "irrigation_d51_d70",
    "rainfall_d71_d105",
    "irrigation_d71_d105",
    "min_temp_d1_d30",
    "max_temp_d1_d30",
    "min_temp_d31_d60",
    "max_temp_d31_d60",
    "min_temp_d61_d90",
    "max_temp_d61_d90",
    "min_temp_d91_d120",
    "max_temp_d91_d120",
    "wind_speed_d1_d30",
    "wind_speed_d31_d60",
    "wind_speed_d61_d90",
    "wind_speed_d91_d120",
    "relative_humidity_d1_d30",
    "relative_humidity_d31_d60",
    "relative_humidity_d61_d90",
    "relative_humidity_d91_d120",
]
