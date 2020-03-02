# rFactor2-championship-setup

Sets up data necessary for custom drivers in custom championships. For use ideally with Log Analyzer.

How to use:
    - Download the latest version of python from https://www.python.org/
	- After cloning/downloading the github files, first edit the settings.json file, vehicles.txt file, and drivers.csv file
	- Then execute main.py with the command python main.py

### settings.json

This file sets some variables and file/folder paths that the program requires. These are explained below:

| Argument | Meaning | Example |
| ------ | ------ | ------ |
| modified | False by default. Prevents script being run without user having edited paths | "True" |
| cship_name | User provided name for the championship. Only used to create separate folders so the script can be re-run for different car combinations | "GT3 Championship #1" |
| resolve_missing_file_method | Default is skip, currently this has no practical effect and should be left untouched | "skip" |
| vehicle_dir | This should be the full path to the /Installed/Vehicles folder in your rFactor 2 installation | "C:/Program Files (x86)/Steam/steamapps/common/rFactor 2/Installed/Vehicles" (steam installation) |
| output_dir | This is the full path to the folder you want to store output files in. You should create this folder before running. I'd suggest creating this folder in your documents folder (although it should work anywhere you can create a folder without admin priviliges) e.g. Documents/RF2/ or  Documents/RF2 cshipmaker files/ etc | "C:/Users/~/Documents/RF2" |
| mod_mgr_path | This is the full path of the mod_mgr executable found in your rFactor 2 installation under /rFactor 2/bin32/ModMgr.exe | "C:/Program Files (x86)/Steam/steamapps/common/rFactor 2/Bin32/ModMgr.exe" (steam installation) |

### vehicles.txt

In this text file you should enter, one line at a time, the vehicles that you want to be included in the championship, using the folder names used in your rFactor 2 installation under \~/rFactor 2/Installed/Vehicles.

Example:
```sh
AstonMartin_Vantage_GT3_2019
Audi_R8LMS_GT3_2019
Audi_R8LMS_GT3_2018
Bentley_Continental_GT3_2017
BMW_M6_GT3_2018
Callaway_Corvette_GT3_2017
McLaren_650S_GT3_2017
McLaren_720S_GT3_2018
Mercedes_AMG_GT3_2017
Porsche_911_GT3_R_2018
Radical_RXC_GT3_2017
```

### drivers.csv

In this file you should enter the information of the drivers you want to be in the championship. This is a csv file, with the first line representing the header, so drivers should be entered one line at a time, with each variable corresponding in position to the header format, and separated by a comma. And explanation of the variables and an example are provided below:

| Variable | Meaning | Example |
| ------ | ------ | ------ |
| First | The drivers first name | Sebastian |
| Last | The drivers last name | Vettel |
| Number | The drivers number (must be unique) | 5 |
| Class | The class of car the driver is driving (no spaces) | GT3 |
| Category | The category of drivers the driver is in, shown in car selection screen i.e. all cars will be listed under this so should be the same for all drivers (no spaces) | GT3_Cars_F1_2020_Grid |
| Team | The drivers team | Scuderia Ferrari |
| Unique ID | Unique ID of car and skin driver will use. This will be the folder name of the car plus the folder name of the skin, joined with a colon | AstonMartin_Vantage_GT3_2019:am_stop_89 |
| Speed | How close to optimally the driver drives (0-100). A setting of 0 corresponds to driving 90% of the optimal, with an increase of 1 in this setting representing an increase of 0.1% up to 100. May require some playing around. | 98 |
| Qualify Speed | How well the driver qualifies (0-100) | Most likely a function of optimal qualifying pace but I'm not sure. May require some playing around. | 98 |
| Wet Speed | How well the driver drives in the wet (0-100). Most likely a function of the optimal wet performance but I'm not sure. May require some playing around. | 95 |
| Aggression | How aggressive the driver is (0-100). A more aggressive driver will give less room, try to pass more frequently, and increase the threshold before they give up a pass. This is affected by the overall ai aggression setting in the ui, so the final aggression is +- up to 20% of the overall value (ie 0 is -20 of overall, 50 is same as overall, 100 is +20 of overall | 60 |
| Composure | How composed the driver is (0-100). Lower numbers increase the frequency of mistakes (if AI Mistakes is >0 in the playerfile) and decrease the time between bad driving zones | 84 |
| Crash | Percentage chance of a driver crashing in a skipped session (0-100) | 0 |
| Completed Laps | Percentage of laps on average a driver completes in a skipped session | 100 |
| Min Racing Skill | The drivers minimum skill (0-100). If AI Limiter > 0.0 in playerfile, then drivers go through cycles of optimal driving and sub-optimal driving, where their driving skill falls to minracingskill*speed | 95 |
| Start Skill | How well the driver gets off the start line (0-100). Relative to a perfect start. Higher values mean the driver will react faster and have better inputs for best grip | 90 |
| Recovery | Deprecated | 100 |
| Reputation | Deprecated | 100 |
| Courtesy | Deprecated | 100 |