import argparse

from handle_database import DatabaseOperations

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
db_operations = DatabaseOperations("codam_corona_tracker", "hilmi", "hilmi")

# Create the query
query_login = "select * from test_host where login = \'{}\'".format(
    args.infected_person_login)
print(query_login)

# Store all the data of the infected person
data = db_operations.read_data(query_login)
print(data)

# Find for each login session of the infected person, which hosts where nearby


# Make query to all those hosts within timeframe of log in period of infected person
