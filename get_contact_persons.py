import argparse
import readline
from typing import Dict, List

from handle_database import OperationsDatabase

# Create an instance of DatabaseOperations to query some data from the database
db_operations = OperationsDatabase("codam_corona_tracker", "data", "hilmi", "hilmi")

# Parse the command line arguments
parser = argparse.ArgumentParser(
    description="List people that sat close to a recently infected person at Codam.")
parser.add_argument("infected_person_login", type=str,
                    help="The intra login of the infected person.")
parser.add_argument("day_positive", type=str,
                    help="The day the person tested positive. Format: day-month-year e.g. 09-12-2021.")
args = parser.parse_args()
print(f"{args.infected_person_login} tested positive on {args.day_positive}.")

# Create the query
query_login = "select * from {} where login = \'{}\'".format(db_operations.table_name,
    args.infected_person_login)
print(query_login)

# Store all the data of the infected person
data: List[Dict] = db_operations.read(query_login)

# Find for each login session of the infected person, which hosts where nearby
for session in data: # loops over the sessions of the infected person
	contacts = input("Which computers do you want to check?\nEnter the hostnames separated by spaces: ").split(" ")
	if (session["login"] in contacts):
		contacts.remove(session["login"])
	for contact in contacts: # loops over all hosts close to this specific session of the infected person
		contact_query = """
		select * from {0} where (host = \'{1}\') and ((begin_at between \'{2}\' and \'{3}\') or (end_at between \'{2}\' and \'{3}\'))
		""".format(db_operations.table_name, contact, session["begin_at"], session["end_at"])
		data_on_contact_person = db_operations.read(contact_query) # could be more people sitting on same computer
		print(data_on_contact_person)
