from shutil import copy

def delete_existing_dirs():
	pass

def create_driver_dirs(drivers):
	
	for d in drivers:
		# Create car directory
		car_dir = Path('.', player_dir, d.car)
		if not os.exists(car_dir):
			os.makedirs(car_dir)

		# Create ai directory
		ai_dir = Path('.',player_dir,driver.car,driver.first + " " + driver.last)
		os.makedirs(ai_dir)

		# Copy vehicle files
		car_files = os.listdirs(Path(vehicle.dir, driver.car, driver.folder))
		for i in car_files:
			i.lower()
		### file idx
		print(f"Copying {driver.first} {driver.last}")
		copy(, ai_dir)

		return None

def create_rcd_idx(drivers):
	for idx, driver in enumerate(drivers):
		driver.idx = idx

def create_rcd_file(driver):
	
	rcd = ""
	rcd.join("\n", 
		[
		"//[[gMa1.002f (c)2016 ]] [[ ]]", 
		driver.car_class, 
		"{", 
		driver.first + " " + driver.last, 
		"{", 
		"Team = " + driver.team, 
		"Component = " + driver.car, 
		"Skin = alt.dds", 
		"VehFile = " + driver.vehicle_file
		"Description = " + "#" + driver.number + " " + driver.car.replace("_", " "),
		"Number = " + driver.number,
		"Classes = " + driver.car_class + " " + driver.car_category,
		"Category = " + driver.car_category,
		"Aggression = " + driver.aggression,
		"Reputation = " + driver.reputation,
		"Courtesy = " + driver.courtesy,
		"Composure = " + driver.composure,
		"Speed = " + driver.speed,
		"QualifySpeed = " + driver.qualify_speed,
		"WetSpeed = " + driver.wet_speed,
		"StartSkill = " + driver.startskill,
		"Crash = " + driver.crash,
		"Recovery = " + driver.recovery,
		"CompletedLaps = " + drivers.completed_laps,
		"MinRacingSkill = " + driver.min_racing_skill,
		"}",
		"}"
		])

	file_name = driver.idx + ".rcd"
	with open(player_dir + driver.car + "/" + file_name, 'w') as file:
		file.write(rcd)
		file.close()

	return None
	
def set_up_ai(drivers):
	delete_existing_dirs()
	create_driver_dirs(drivers)
	create_rcd_idx(drivers)
	for driver in drivers:
		create_rcd_file(driver)

	return None

