import time
from typing import List, Dict
from get_user_data import API42
from handle_database import DatabaseOperations

# Set interval variable for while loop in seconds
# If someone logs in and off in less time than the interval perdiod, that person will not be registered
interval = 60

# Instantiate a DatabaseOperations object to handle MySQL
db_operations = DatabaseOperations("codam_corona_tracker", "hilmi", "hilmi")

# Instantiate an API42 object for handling API requests
api = API42()
payload = {"filter[campus_id]": 14,
		   "filter[active]": "true", "page[size]": 100}

# Continuously get data from the API and put into database
while True:
	data: List[Dict] = api.get("locations", payload)  # data is a list

	# Get active people data
	logged_in: List[Dict] = db_operations.get_active_students(data)
	print(f"Currently active students:\n{logged_in}")

	# Get the recently logged off sessions
	logged_off: List[Dict] = db_operations.get_recently_logged_off(logged_in)

	# Check whether someone logged off, if so, query and add to the database
	who_logged_off: List[Dict] = []
	for user in logged_off:
		tmp_payload = payload
		tmp_payload["filter[id]"] = user["id"]
		who_logged_off.extend(api.get("locations", tmp_payload))
	print(
		f"Users who logged off in the last {interval} seconds: {who_logged_off}")
	print("")

	# If someone logged off, insert data into database
	db_operations.insert_data(who_logged_off)

	# Remove old entries from the database
	db_operations.remove_old_data(1, "hour") # for now it will only print

	db_operations.active = logged_in
	time.sleep(interval)
