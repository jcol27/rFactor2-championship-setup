import os
from pathlib import Path
import json
import csv
import subprocess
import unpack.py
import ai_setup.py

# Read in data from config files
vehicle_dir, output_dir, mod_mgr_path = read_json()
drivers = read_csv()
vehicles = read_txt()

# Unpack all vehicles
get_vehicles()

# 

