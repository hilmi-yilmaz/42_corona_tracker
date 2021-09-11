import argparse

from handle_database import DatabaseOperations

# Parse the command line arguments
parser = argparse.ArgumentParser(description="List people that sat close to a recently infected person at Codam.")
parser.add_argument("infected_person_login", type=str, help="The intra login of the infected person.")
parser.add_argument("day_positive", type=str, help="The day the person tested positive. Format: day-month-year e.g. 09-12-2021.")
args = parser.parse_args()
print(f"{args.infected_person_login} tested positive on {args.day_positive}.")

# Create an instance of DatabaseOperations to query some data from the database
db_operations = DatabaseOperations("codam_corona_tracker", "hilmi", "hilmi")

# Create the query
query_login = "select * from test_host where login = \'{}\'".format(args.infected_person_login)
print(query_login)

# Store all the data of the infected person
data = db_operations.read_data(query_login)
print(data)