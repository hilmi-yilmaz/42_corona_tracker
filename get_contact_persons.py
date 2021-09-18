import argparse
import readline
from datetime import datetime
from typing import Dict, List

from handle_database import OperationsDatabase

# Create an instance of DatabaseOperations to query some data from the database
db_operations = OperationsDatabase("codam_corona_tracker", "data", "hilmi", "hilmi")

# Parse the command line arguments
parser = argparse.ArgumentParser(
    description="List people that sat close to a recently infected person at Codam.")
parser.add_argument("infected_person_login", type=str,
                    help="The intra login of the infected person.")
parser.add_argument("day_positive", type=lambda s: datetime.strptime(s, '%d-%m-%Y').date(),
                    help="The day the person tested positive. Format: day-month-year e.g. 09-12-2021.")
args = parser.parse_args()

# Create the query
query_login = "select * from {} where login = \'{}\'".format(db_operations.table_name,
    args.infected_person_login)
print(query_login)

# Store all the data of the infected person
infected_person_data: List[Dict] = db_operations.read(query_login)

# Print information
print(f"Information of contact persons of {args.infected_person_login} who got infected on {args.day_positive}.")

# Find for each login session of the infected person, which hosts where nearby
for infected_person_session in infected_person_data: # loops over the sessions of the infected person
	contact_data = input("Which computers do you want to check?\nEnter the hostnames separated by spaces: ").split(" ")
	# print(contact_data)
	# print(infected_person_session["login"])
	if (infected_person_session["host"] in contact_data):
		contact_data.remove(infected_person_session["host"])
	for contact in contact_data: # loops over all hosts close to this specific session of the infected person
		contact_query = """
		select * from {0} where (host = \'{1}\') and (date(begin_at) = \'{2}\')
		""".format(db_operations.table_name, contact, args.day_positive)
		data_on_contact_persons = db_operations.read(contact_query)
		for loggins in data_on_contact_persons:
			overlap = min(infected_person_session["end_at"], loggins["end_at"]) - max(infected_person_session["begin_at"], loggins["begin_at"])
			if overlap.days >= 0:
				print("{} was logged in {} (hours:minutes:seconds) sitting on computer {} on {}.".format(loggins["login"], overlap, loggins["host"], loggins["begin_at"].date()))
