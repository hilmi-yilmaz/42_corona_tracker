import argparse
import readline
import time
from datetime import datetime, timedelta
from typing import Dict, List

from get_user_data import API42

# Create an instance of DatabaseOperations to query some data from the database
api = API42()

# Parse the command line arguments
parser = argparse.ArgumentParser(
    description="List people that sat close to a recently infected person at Codam.")
parser.add_argument("infected_person_login", type=str,
                    help="The intra login of the infected person.")
parser.add_argument("day_positive", type=lambda s: datetime.strptime(s, '%d-%m-%Y').date(),
                    help="The day the person tested positive. Format: day-month-year e.g. 09-12-2021.")
args = parser.parse_args()

# Get user's user_id


# Create the payload to send with the request to get all data one day before infection
begin_at_range = "{},{}".format((args.day_positive - timedelta(days=1)).strftime("%Y-%m-%dT%H:%M:%SZ"), args.day_positive.strftime("%Y-%m-%dT%H:%M:%SZ"))
print(begin_at_range)
payload = {"filter[campus_id]": api.campus_id, "range[begin_at]": begin_at_range, "page[size]": 100}


# Get data from api
data = api.get("locations", payload)
# i = 0
# for element in data:
# 	print(element)
# 	print("")
# 	i += 1
# print(i)

# Get the sessions of the infected_person
infected_person_all_sessions = [session for session in data if args.infected_person_login == session["user"]["login"]]
print(infected_person_all_sessions)

for infected_person_session in infected_person_all_sessions:
	contact_hosts: List[str] = input(
		"Which computers do you want to check?\nEnter the hostnames separated by spaces: ").split(" ")
	if infected_person_session["host"] in contact_hosts:
		contact_hosts.remove(infected_person_session["host"])
	for host in contact_hosts:
		contact_payload = payload.copy()
		contact_payload["filter[host]"] = host
		contact_data = api.get("locations", contact_payload)
		print(contact_data)
		print(len(contact_data))
		time.sleep(1)

exit(0)

# Create the query
query_login = "select * from {} where login = \'{}\'".format(db_operations.table_name,
                                                             args.infected_person_login)
print(query_login)

# Store all the data of the infected person
infected_person_data: List[Dict] = db_operations.read(query_login)

# Print information
print(
    f"Information of contact persons of {args.infected_person_login} who got infected on {args.day_positive}.")

# Find for each login session of the infected person, which hosts where nearby
for infected_person_session in infected_person_data:  # loops over the sessions of the infected person
    contact_data: List[str] = input(
        "Which computers do you want to check?\nEnter the hostnames separated by spaces: ").split(" ")
    if infected_person_session["host"] in contact_data:
        contact_data.remove(infected_person_session["host"])
    for contact in contact_data:
        contact_query = """
		select * from {0} where (host = \'{1}\') and (date(begin_at) = \'{2}\')
		""".format(db_operations.table_name, contact, args.day_positive)
        data_on_contact_persons = db_operations.read(contact_query)
        for loggins in data_on_contact_persons:
            overlap = min(infected_person_session["end_at"], loggins["end_at"]) - max(
                infected_person_session["begin_at"], loggins["begin_at"])
            if overlap.days >= 0:
                print("{} was logged in {} (hours:minutes:seconds) sitting on computer {} on {}.".format(
                    loggins["login"], overlap, loggins["host"], loggins["begin_at"].date()))
