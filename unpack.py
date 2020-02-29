import os
from pathlib import Path
import json
import csv
import subprocess
from shutil import copy, rmtree

import sys

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
		self.start_skill = start_skill

	def set_vehicle_file(self, dir):
		self.vehicle_file = dir

# Helper function to check if string represents an int
def represents_int(li):
	for s in li:
		try:
			int(s)
		except ValueError:
			return False
	return True

# Read in settings from json
def read_json():
	with open("settings.json") as file:
		data = json.load(file)
	file.close()
	modified = data["modified"]
	if modified == "True":
		cship_name = data["cship_name"]
		vehicle_dir = data["paths"]["vehicle_dir"]
		output_dir = data["paths"]["output_dir"]
		mod_mgr_path = data["paths"]["mod_mgr_path"]
		temp_dir = data["paths"]["temp_dir"]
		return [modified, cship_name, vehicle_dir, output_dir, mod_mgr_path, temp_dir]
	return [modified]

# Read in data from csv, returns list of driver objects
def read_csv():
	drivers = []
	with open('drivers.csv') as file:
		code = "pass"
		csv_reader = csv.reader(file, delimiter=',')
		next(csv_reader)
		for row in csv_reader:
			try:	
				drivers.append(Driver(row[0], row[1], row[2], row[3], row[4], row[5], row[6], row[7], row[8], row[9], row[10]))
			except:
				code = "err"
	return code, drivers

# Read in vehicles, returns list of strings
def read_txt():
	with open('vehicles.txt', 'r') as file:
		vehicles = []
		for line in file:
			line.replace("\"", "")
			line = line.rstrip()
			vehicles.append(line)
	return vehicles

# Get list of models
def get_models(vehicle_dir):
	models = os.listdir(vehicle_dir)
	return models

# Get latest version of vehicle
def get_latest_version(vehicle_dir, vehicle):
	ver_list = os.listdir(Path(vehicle_dir, ".", vehicle))
	ver_list_floats = [float(i) for i in ver_list]
	return str(max(ver_list_floats))

# Unpacks the .mas object for a given vehicle and stores it in temp_dirs
def unpack_mas(vehicle, vehicle_dir, temp_dir, mod_mgr_path, mas = "car-upgrade.mas"):
	unpack_file_types = ["*.veh", "*.dds", "*.json"]
	s = " "
	s = s.join(unpack_file_types)
	models = get_models(vehicle_dir)
	latest_version = get_latest_version(vehicle_dir, vehicle)
	extract_path = "\"" + vehicle_dir + "/" + vehicle + "/" + latest_version + "/" + mas + "\""
	try:
		command = "\"" + mod_mgr_path + "\" " + s + " -x" + extract_path + " -o\"" + temp_dir + "\""
		print(command)
		subprocess.run(command)
	except:
		print("Error calling mod_mgr.exe. Check paths given in settings.json and retry")
		sys.exit()
	
	return None

# Extracts vehicle info from vehicle_contents
def extract_vehicle_info(vehicle_contents, tag):
	pass

# Extracts vehicles
def get_vehicles(vehicle_dir, temp_dir, output_dir, vehicles, mod_mgr_path):
	
	# Create empty temp folder
	if os.path.exists(Path(temp_dir)):
		rmtree(temp_dir)
		os.makedirs(temp_dir)
	else:
		os.makedirs(temp_dir)

	vehicle_inventory = {}
	for vehicle in vehicles:
		# Unpack vehicle
		unpack_mas(vehicle, vehicle_dir, temp_dir, mod_mgr_path, mas = "car_upgrade.mas")

		# Get all vehicle files and catalog all extracted files
		all_files = os.listdir(temp_dir)
		all_files = [x.lower() for x in all_files]
		veh_files = [x for x in all_files if x.count(".veh") != 0]

		# Loop over vehicle files to extract info
		veh_files_dicts = {}
		for idx, veh in enumerate(veh_files):
			try:
				veh_dict = {}
				with open(temp_dir + veh) as file:
					veh_contents = readLines(files)
					veh_dict["idx"] = idx
					veh_dict["dds_file"] = extract_vehicle_info(veh_contents, "DefaultLivery=.*dds\"")
					veh_dict["team"] = extract_vehicle_info(veh_contents, "Team=.*\"")
					veh_dict["full_team_name"] = extract_vehicle_info(veh_contents, "FullTeamName=.*\"")
					veh_base = veh.replace(".dds","")
					veh_dict["dds_region_file"] = veh_base + "_region.dds"
					veh_dict["json_file"] = veh_base + ".json"
					veh_dict["veh_folder"] = veh_base

			except:
				print("Error in reading .veh files. If you see this error something has probably gone seriously wrong.")
				sys.exit()
			veh_files_dicts[idx] = veh_dict

		# Clean directory before file copy
		if os.path.exists(output_dir):
			rmtree(output_dir)
			os.makedirs(output_dir)

		# File copy
		copy_dir = Path(output_dir, vehicle, veh_files_dicts["veh_folder"])
		os.makedirs(copy_dir)
		shutil.copy(Path(temp_dir, veh), copy_dir)
		shutil.copy(Path(temp_dir, veh_dict["dds_file"]), copy_dir)
		shutil.copy(Path(temp_dir, veh_dict["dds_region_file"]), copy_dir)
		shutil.copy(Path(temp_dir, veh_dict["json_file"]), copy_dir)

		# Write veh_files_dict to vehicle_inventory
		vehicle_inventory[vehicle] = veh_files_dicts

	# Delete temp directory
	if os.exists(temp_dir):
		shutil.rmtree(temp_dir)
	
	# Write vehicle inventory
	with open("vehicle_inventory.json", "-w", encoding="uft-8") as file:
		json.dump(vehicle_inventory, file, ensure_ascii=False, indent=4)

	return None
