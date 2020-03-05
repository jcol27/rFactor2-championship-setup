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
if type(json_data) == list:
	print("Error reading json file. Please edit this file to contain the correct paths, check that all paths are valid and exist, then change \"modified\" to \"True\"")
	sys.exit()
elif not os.path.exists(json_data["vehicle_dir"]) or not os.path.exists(json_data["player_dir"]) or not os.path.exists(json_data["output_dir"]) or not os.path.exists(json_data["mod_mgr_path"]):
	print("Error reading json file. Please edit this file to contain the correct paths, check that all paths are valid and exist, then change \"modified\" to \"True\"")
	sys.exit()	
else:
	modified = json_data["modified"]
	cship_name = json_data["cship_name"]
	resolve_missing_file_method = json_data["resolve_missing_file_method"]
	vehicle_dir = json_data["vehicle_dir"]
	output_dir = json_data["output_dir"]
	output_vehicle_dir = json_data["output_dir"] + "/" + "Vehicles" + "/" + cship_name
	unpack.create_dir(output_vehicle_dir)
	mod_mgr_path = json_data["mod_mgr_path"]
	temp_dir = json_data["output_dir"] + "/" + "Temp"
	player_dir = json_data["player_dir"]


# Gets list of drivers (list of objects of class Driver)
code, drivers = unpack.read_csv()

# Check if any errors reading data.csv file
if code == "err":
	print("Error reading data.csv. Probably due to empty cells or unfinished lines")
	sys.exit()

for driver in drivers:
	if not unpack.represents_int([driver.speed, driver.qualify_speed, driver.wet_speed, driver.aggression, driver.composure, driver.crash, driver.completed_laps, driver.min_racing_skill, driver.start_skill, driver.recovery, driver.reputation, driver.courtesy]):
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
unpack.get_vehicles(vehicle_dir, temp_dir, output_vehicle_dir, vehicles, mod_mgr_path, resolve_missing_file_method)

# Set up ai
ai_setup.set_up_ai(drivers, vehicles, output_vehicle_dir, player_dir, vehicle_dir)