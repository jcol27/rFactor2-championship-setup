from shutil import copy, rmtree
import os
from pathlib import Path
import sys

def delete_existing_dirs(vehicles, player_dir):
	for vehicle in vehicles:
		if os.path.exists(Path(player_dir, vehicle)):
			rmtree(Path(player_dir, vehicle))

	return None

def create_driver_dirs(drivers, player_dir, output_vehicle_dir):
	
	for driver in drivers:
		# Create car directory
		car_dir = Path(player_dir, driver.car_folder_name)
		if not os.path.exists(car_dir):
			os.makedirs(car_dir)

		# Create ai directory
		ai_dir = Path(player_dir, driver.car_folder_name, driver.first + " " + driver.last)
		os.makedirs(ai_dir)

		# Copy vehicle files
		car_files = os.listdir(Path(output_vehicle_dir, driver.car_folder_name, driver.skin_folder_name))
		for i in car_files:
			copy(Path(output_vehicle_dir, driver.car_folder_name, driver.skin_folder_name, i), ai_dir)
		### file idx
		print(f"Copying {driver.first} {driver.last}")

	return None

def create_rcd_idx(drivers):
	for idx, driver in enumerate(drivers):
		driver.idx = idx

def create_rcd_file(driver, player_dir):
	
	rcd = "\n"
	seq = ("//[[gMa1.002f (c)2016 ]] [[ ]]", 
		driver.drclass, 
		"{", 
		driver.first + " " + driver.last, 
		"{", 
		"Team = " + driver.team, 
		"Component = " + driver.car_folder_name, 
		"Skin = alt.dds", 
		"VehFile = " + driver.vehicle_file,
		"Description = " + "#" + driver.number + " " + driver.car_folder_name.replace("_", " "),
		"Number = " + driver.number,
		"Classes = " + driver.drclass + " " + driver.category,
		"Category = " + driver.category,
		"Aggression = " + driver.aggression,
		"Reputation = " + driver.reputation,
		"Courtesy = " + driver.courtesy,
		"Composure = " + driver.composure,
		"Speed = " + driver.speed,
		"QualifySpeed = " + driver.qualify_speed,
		"WetSpeed = " + driver.wet_speed,
		"StartSkill = " + driver.start_skill,
		"Crash = " + driver.crash,
		"Recovery = " + driver.recovery,
		"CompletedLaps = " + driver.completed_laps,
		"MinRacingSkill = " + driver.min_racing_skill,
		"}",
		"}"
		)
	rcd = rcd.join(seq)

	file_name = str(driver.idx) + ".rcd"
	with open(player_dir + "/" + driver.car_folder_name + "/" + file_name, 'w') as file:
		file.write(rcd)
		file.close()

	return None
	
def set_up_ai(drivers, vehicles, output_vehicle_dir, player_dir, vehicle_dir):
	for driver in drivers:
		driver.set_vehicle_file(output_vehicle_dir)
	delete_existing_dirs(vehicles, player_dir)
	create_driver_dirs(drivers, player_dir, output_vehicle_dir)
	create_rcd_idx(drivers)
	for driver in drivers:
		create_rcd_file(driver, player_dir)

	return None

