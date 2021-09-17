import argparse

from handle_database import OperationsDatabase

# Parse the command line arguments
parser = argparse.ArgumentParser(
    description="List people that sat close to a recently infected person at Codam.")
parser.add_argument("infected_person_login", type=str,
                    help="The intra login of the infected person.")
parser.add_argument("day_positive", type=str,
                    help="The day the person tested positive. Format: day-month-year e.g. 09-12-2021.")
parser.add_argument("hosts", type=str, nargs='*',
					help="The hosts we want to gather data from.")
args = parser.parse_args()
print(f"{args.infected_person_login} tested positive on {args.day_positive}.")
print(f"Gathering data from the following hosts: {args.hosts}")

# Create an instance of DatabaseOperations to query some data from the database
db_operations = OperationsDatabase("codam_corona_tracker", "f0r1s8", "hilmi", "hilmi")

# Create the query
query_login = "select * from f0r1s8 where login = \'{}\'".format(
    args.infected_person_login)
print(query_login)

# Store all the data of the infected person
data = db_operations.read(query_login)
print(data)

# Find for each login session of the infected person, which hosts where nearby
for session in data: # loops over the sessions of the infected person
	print(session)
	begin_at = session[2]
	end_at = session[3]
	print(type(begin_at))
	for contact in args.hosts: # loops over all hosts close to this specific session of the infected person
		contact_query = """
		select * from f0r1s8 where (host = \'{}\') and (begin_at or end_at between %s and %s)
		""".format(contact)
		contact_data = [begin_at, end_at]

	print(session)

# Make query to all those hosts within timeframe of log in period of infected person
