from getpass import getpass
import time
from typing import List, Dict
from get_user_data import API42
from handle_database import UpdateDatabase

# Set interval variable for while loop in seconds
# If someone logs in and off in less time than the interval perdiod, that person will not be registered
interval = 60

# Instantiate a DatabaseOperations object to handle MySQL
db_operations = UpdateDatabase("codam_corona_tracker", "data", "hilmi", getpass("Enter database password: "))

# Instantiate an API42 object for handling API requests
api = API42()
payload = {"filter[campus_id]": api.campus_id,
		   "filter[active]": "true", "page[size]": 100}

# Continuously get data from the API and put into database
while True:

	# Get active people data
	logged_in: List[Dict] = api.get("locations", payload)
	print(f"Currently logged in ({len(logged_in)}):")
	for user in logged_in:
		print("{} ({})".format(user["user"]["login"], user["host"]))
	print("")

	# Get the recently logged off sessions
	logged_off: List[Dict] = db_operations.get_recently_logged_off(logged_in)
	print(f"Logged off students ({len(logged_off)}):")
	for user in logged_off:
		print(user["user"]["login"])
	print("")

	# Check whether someone logged off, if so, query and add to the database
	for user in logged_off:
		logged_off_payload = {"filter[campus_id]": api.campus_id,
		   "filter[active]": "false", "page[size]": 100, "filter[id]": user["id"]}
		db_operations.insert_logged_off(api.get("locations", logged_off_payload)[0])
		time.sleep(1)

	# Remove old entries from the database
	db_operations.remove_old_data(3, "day") # for now it will only print

	db_operations.active = logged_in.copy()
	print("------------------------------------------------")
	time.sleep(interval)
