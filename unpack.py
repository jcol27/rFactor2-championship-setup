import os
from pathlib import Path
import json
import csv
import subprocess
from shutil import copy

# Class to store driver attributes
class Driver():
	def __init__(self, first, last, number, team, unique_id, speed, wet_speed, aggression, composure, min_racing_skill, start_skill):
		
		self.first = first
		self.last = last
		self.number = number
		self.team = team
		self.unique_id = unique_id
		self.speed = speed
		self.wet_speed = wet_speed
		self.aggression = aggression
		self.composure = composure
		self.min_racing_skill = min_racing_skill
		self.start_skill

	def set_vehicle_file(self, dir):
		self.vehicle_file = dir

# Read in settings from json
def read_json():
	data = json.load("./settings.json")
	return vehicle_dir, output_dir, mod_mgr_path

# Read in data from csv, returns list of driver objects
def read_csv():
	drivers = []
	with open('./data.csv') as file:
		csv_reader = csv.reader(file, delimiter=',')
		csv_reader.next()
		for row in csv_reader:
			drivers.append(Driver(row[0], row[1], row[2], row[3], row[4], row[5], row[6], row[7], row[8], row[9], row[10]))
	return drivers

# Read in vehicles, returns list of strings
def read_txt():
	with open('./vehicles.txt', 'r') as file:
		vehicles = file.readlines()
	return vehicles

# Get list of models
def get_models(vehicle_dir):
	os.chdir(vehicle_dir)
	models = os.listdir()
	return models

# Get latest version of vehicle
def get_latest_versions(vehicle_dir, vehicle):
	os.chdir(vehicle_dir)
	ver_list = os.listdir(Path(".", vehicle))
	ver_list_floats = [float(i) for i in ver_list]
	return max(ver_list_floats)

# Unpacks the .mas object for a given vehicle and stores it in temp_dirs
def unpack_mas(vehicle, vehicle_dir, temp_dir, mod_mgr_path, mas = "car-upgrade.mas"):
	os.chdir(vehicle_dir)
	unpack_file_types = ["*.veh", "*.dds", "*.json"]
	models = get_models(vehicle_dir)
	latest_version = get_latest_versions(vehicle_dir, models)
	extract_path = Path(".", vehicle, latest_version, mas)
	subprocess.run([mod_mgr_path, unpack_file_types + " -x\"" + extract_path + "\" " + "-o\"" + temp_dir + "\""])
	return None

# Extracts vehicle info from vehicle_contents
def extract_vehicle_info(vehicle_contents, tag):
	pass

# Extracts vehicles
def get_vehicles(vehicle_dir, temp_dir, vehicles, mod_mgr_path):
	os.chdir(temp_dir)
	if not os.exists(Path(".", "temp"))
		os.makedirs(temp_dir)

	vehicle_inventory = []
	for vehicle in vehicles:
		# Unpack vehicle
		unpack_mas(vehicle, vehicle_dir, temp_dir, mod_mgr_path, mas = "car_upgrade.mas")

		# Get all vehicle files and catalog all extracted files
		all_files = os.listdir(temp_dir)
		all_files = [x.lower() for x in all_files]
		vehicle_files = [x in all_files if x.count(".veh") != 0]

		# Loop over vehicle files to extract info
		

		# Start copy (if directory exists clean it)
		if os.exists(output_dir):
			shutil.rmtree(output_dir)
			os.makedirs(output_dir)

	if os.exists(temp_dir):
		shutil.rmtree(temp_dir)

	return None



















			




