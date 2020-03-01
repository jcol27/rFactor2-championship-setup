import os
from pathlib import Path
import json
import csv
import subprocess
from shutil import copy, rmtree
import re
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

# Cleans given directory (loop necessary to catch odd PermissionErrors [WinError 5])
def create_dir(in_dir):
	i = 0
	while i < 100:
		i += 1
		try:
			if os.path.exists(in_dir):
				rmtree(in_dir)
			os.makedirs(in_dir)
		except OSError:
			continue
	return None	

# Read in settings from json
def read_json():
	with open("settings.json") as file:
		data = json.load(file)
	file.close()
	modified = data["modified"]
	if modified == "True":
		cship_name = data["cship_name"]
		resolve_missing_file_method = data["resolve_missing_file_method"]
		vehicle_dir = data["paths"]["vehicle_dir"]
		output_dir = data["paths"]["output_dir"]
		mod_mgr_path = data["paths"]["mod_mgr_path"]
		temp_dir = data["paths"]["temp_dir"]
		return [modified, cship_name, resolve_missing_file_method, vehicle_dir, output_dir, mod_mgr_path, temp_dir]
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
	#unpack_file_types = ["*.veh", "*.dds", "*.json"]
	unpack_file_types = ["*.*"]
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
	# Get label of tag and create regular expression for searching vehicle_contents
	new_tag = tag.split(".")[0]
	new_tag = "(" + new_tag + "\"[^\"]+\")$"
	p = re.compile(new_tag)
	# Search vehicle_contents by line (or technically by list element)
	for string in vehicle_contents:
		match = p.search(string)
		if match:
			# Define new regex for searching match
			q = "(\"[^!@&*]+\")$"
			q = re.compile(q)
			# Extract vehicle info from match string
			result = q.search(match[0])[0]
			result = result.replace("\"","")
			if result == None:
				print("Error extracting vehicle info.")
				sys.exit()
	return result

# Extracts vehicles
def get_vehicles(vehicle_dir, temp_dir, output_dir, vehicles, mod_mgr_path, resolve_missing_file_method):
	
	# Create empty temp folder
	if os.path.exists(Path(temp_dir)):
		rmtree(temp_dir)
		create_dir(temp_dir)
	else:
		create_dir(temp_dir)

	vehicle_inventory = {}
	for vehicle in vehicles:
		# Unpack vehicle
		unpack_mas(vehicle, vehicle_dir, temp_dir, mod_mgr_path, mas = "car-upgrade.mas")

		# Get all vehicle files and catalog all extracted files
		all_files = os.listdir(temp_dir)
		all_files = [x.lower() for x in all_files]
		veh_files = [x for x in all_files if x.count(".veh") != 0]

		# Loop over vehicle files to extract info
		veh_files_dicts = {}
		for idx, veh in enumerate(veh_files):
			try:
				veh_dict = {}
				with open(temp_dir + "/" + veh) as file:
					veh_contents = file.readlines()
					veh_dict["idx"] = idx
					veh_dict["veh_file"] = veh
					veh_dict["dds_file"] = extract_vehicle_info(veh_contents, "DefaultLivery=.*dds\"")
					veh_dict["team"] = extract_vehicle_info(veh_contents, "Team=.*\"")
					veh_dict["full_team_name"] = extract_vehicle_info(veh_contents, "FullTeamName=.*\"")
					veh_base = veh_dict["dds_file"][:-4]
					veh_dict["veh_base"] = veh_base
					veh_dict["dds_region_file"] = veh_base + "_region.dds"
					veh_dict["json_file"] = veh_base + ".json"
					veh_dict["veh_folder"] = veh_base.lower()
					veh_dict["png_file"] = "na"
					p = veh_base.lower() + "[^!@]+icon[.]png$"
					p = re.compile(p)
					match = None
					for file in all_files:
						m = p.search(file.lower())
						if m != None:
							veh_dict["png_file"] = m[0].replace("\"","")


			except Exception as err:
				print(err)
				if err == PermissionError:
					print("Permission error in creating directory")
				else:
					print(err)
					print("Error in reading .veh files. If you see this error something has probably gone seriously wrong.")
				sys.exit()
			veh_files_dicts.update({str(idx): veh_dict})

		# Clean directory before file copy
		if not os.path.exists(output_dir):
			create_dir(output_dir)

		# File copy
		skipped = []
		for idx, veh_dict in enumerate(veh_files_dicts.values()):
			#print(type(veh_dict))
			#print(f"veh_dict = {veh_dict}")
			copy_dir = Path(output_dir, vehicle, veh_files[idx][:-12])
			create_dir(copy_dir)
			copy(Path(temp_dir, veh_files[idx]), copy_dir)
			copy(Path(temp_dir, veh_dict["dds_file"]), Path(copy_dir, "alt.dds"))

			if veh_dict["png_file"] != "na":
				copy(Path(temp_dir, veh_dict["png_file"]), Path(copy_dir, veh_dict["veh_base"] + ".png"))
			# Try except block for copying .json to allow for missing file
			try:
				copy(Path(temp_dir, veh_dict["json_file"]), Path(copy_dir, "alt.json"))
			except:
				if resolve_missing_file_method == "replace_with_default":
					continue
					#vehicle
					#copy(, copy_dir)
				else: 
					rmtree(copy_dir)
					skipped.append(str(idx))
					continue

			# Try except block for copying _region.dds file to allow for missing file
			try:
				copy(Path(temp_dir, veh_dict["dds_region_file"]), Path(copy_dir, "alt_region.dds"))
			except:
				if resolve_missing_file_method == "replace_with_default":
					continue
					#vehicle
					#copy(, copy_dir)
				else: 
					rmtree(copy_dir)
					skipped.append(str(idx))
					continue

		# Remove skipped veh_dicts from veh_files_dicts
		for string in skipped:
			useless = veh_files_dicts.pop(string)

		# Write veh_files_dict to vehicle_inventory
		vehicle_inventory[vehicle] = veh_files_dicts

		# Clean temp directory
		create_dir(temp_dir)

	# Delete temp directory
	if os.path.exists(temp_dir):
		rmtree(temp_dir)
	
	# Write vehicle inventory
	with open("vehicle_inventory.json", "w") as file:
		json.dump(vehicle_inventory, file, ensure_ascii=False, indent=4)

	return None
