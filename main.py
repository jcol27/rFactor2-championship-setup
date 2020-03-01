import os
from pathlib import Path
import json
import csv
import subprocess
import unpack
import ai_setup
import sys

# Read in data from config files (dictionary)
json_data = unpack.read_json()

# Catches for incorrect input in settings.json
if len(json_data) == 1 or not os.path.exists(json_data[3]) or not os.path.exists(json_data[4]) or not os.path.isfile(json_data[5] or not os.path.exists(json_data[6])):
	print("Error reading json file. Please edit this file to contain the correct paths, check that all paths are valid and exist, then change \"modified\" to \"True\"")
	sys.exit()
else:
	modified = json_data[0]
	cship_name = json_data[1]
	resolve_missing_file_method = json_data[2]
	vehicle_dir = json_data[3]
	output_dir = json_data[4] + "/" + cship_name
	unpack.create_dir(output_dir)
	mod_mgr_path = json_data[5]
	temp_dir = json_data[6]


# Gets list of drivers (list of objects of class Driver)
code, drivers = unpack.read_csv()

# Check if any errors reading data.csv file
if code == "err":
	print("Error reading data.csv. Probably due to empty cells or unfinished lines")
	sys.exit()

for driver in drivers:
	if not unpack.represents_int([driver.speed, driver.wet_speed, driver.aggression, driver.composure, driver.min_racing_skill, driver.start_skill]):
		print(f"Error reading data.csv. One driver attribute of \"{driver.first} {driver.last}\" that should be int is not.")
		sys.exit()
	
# Gets list of vehicles (list of strings)
vehicles = unpack.read_txt()

if len(vehicles) == 0:
	print("Error reading vehicles.txt. File is empty")
	sys.exit()

# Get list of models from vehicle_dir
models = unpack.get_models(vehicle_dir)

# Check if strings in vehicles match models
for v in vehicles:
	match = 0
	for m in models:
		if v == m:
			match += 1
	if match != 1:
		print(f"Error reading vehicles.txt. {v} is in vehicles.txt but is not found in {vehicle_dir}")
		sys.exit()

# Unpack all vehicles
unpack.get_vehicles(vehicle_dir, temp_dir, output_dir, vehicles, mod_mgr_path, resolve_missing_file_method)

# Set up ai
