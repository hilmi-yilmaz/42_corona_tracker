import time

from get_user_data import API42
from handle_database import DatabaseOperations

# Instantiate a DatabaseOperations object to handle MySQL
db_operations = DatabaseOperations("codam_corona_tracker", "hilmi", "hilmi")

# Instantiate an API42 object for handling API requests 
api = API42()
payload = {"filter[campus_id]":14, "filter[active]": "true", "page[size]": 50}

# Continously get data from the API and put into database
while True:
    data = api.get("locations", payload) # data is a list

    # Get the active people data
    currently_active = db_operations.get_active_students(data)
    print(currently_active)

    # Get the recently logged off session
    logged_off = db_operations.get_recently_logged_off(currently_active)

    # Check whether someone logged off, if so, query and add to the database
    for session in logged_off:
        tmp_payload = payload
        tmp_payload["filter[id]"] = session
        who_logged_off = api.get("locations", tmp_payload)
        print(who_logged_off)

    db_operations.insert_data(data, currently_active)

    db_operations.active = currently_active
    time.sleep(60)