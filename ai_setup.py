from shutil import copy

def delete_existing_dirs():
	pass

def create_dirs(drivers):
	'''
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
	'''
	pass


def create_rcd_file(driver):
	'''
	rcd = ""
	rcd.join("\n", 
		[
		"//[[gMa1.002f (c)2016    ]] [[            ]]", 
		"GT3", 
		"{", 
		driver.first + " " + driver.last, 
		"{", "Team = " + driver.team, 
		"Component = " + driver.car, 
		"Skin = alt.dds", 
		"VehFile = " + driver.vehicle_file
		"Description = " + "#" + driver.number + " " + driver.car.replace("_", " "),
		"Number = " + driver.number,
		"Classes = " + car_class,
		"Category = " + car_class.replace("_", " "),
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

	file_name = driver.rcd_num + ".rcd"
	with open(player_dir + driver.car + "/" + file_name, 'w') as file:
		file.write(rcd)
		file.close()

	return None
	'''
	pass

