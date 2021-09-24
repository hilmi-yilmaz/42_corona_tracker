import argparse
from datetime import datetime, timedelta
from typing import List, Dict

from corona_tracker_42.api42_wrapper import API42
from corona_tracker_42.get_contacts import InfectedStudent
from corona_tracker_42.utils import *

# Parse the command line arguments
parser = argparse.ArgumentParser(
    description="List people that sat close to a recently infected person at Codam.")
parser.add_argument("infected_person_login", type=str,
                    help="The intra login of the infected person.")
parser.add_argument("day_positive", type=lambda s: datetime.strptime(s, '%d-%m-%Y').date(),
                    help="The day the person tested positive. Format: day-month-year e.g. 09-12-2021.")
parser.add_argument("days_to_check", type=int,
                    help="For how many previous days to check.")
args = parser.parse_args()

# Create an API42 object to make calls with
api = API42()

# Get data from the API from the past few days
date_range: str = "{},{}".format((args.day_positive - timedelta(days=args.days_to_check)).strftime("%Y-%m-%dT%H:%M:%SZ"), args.day_positive.strftime("%Y-%m-%dT%H:%M:%SZ"))
payload = {"filter[campus_id]": api.campus_id, "range[begin_at]": date_range, "page[size]": 100}
data: List[Dict] = api.get("locations", payload)

# Create an object containing information on the student
infected_student = InfectedStudent(args.infected_person_login, args.day_positive, args.days_to_check)

# Get sessions of the infected person
infected_student.get_sessions(data)

print(infected_student.login)
print(infected_student.session_id)
print(infected_student.host)
print(infected_student.begin_at)
print(infected_student.end_at)
print(infected_student.day_positive)
print(infected_student.days_to_check)


# Get people who sat close to infected person

def get_contacts_1(student):

	i = 0
	map_host_to_contacts: Dict[str, List] = {}
	for i in range(len(student.session_id)):
		
		print("Session {} on host {} from {} until {}".format(
		i, student.host[i], student.begin_at[i], student.end_at[i]))

		if student.host[i] in map_host_to_contacts:
			contact_hosts = map_host_to_contacts[student.host[i]]
		else:
			contact_hosts: List[str] = input(
				"Which computers do you want to check?\nEnter the hostnames separated by spaces: ").split(" ")
			# Remove duplicate elements
			contact_hosts = list(dict.fromkeys(contact_hosts))
			# Remove host itself if given as input
			if student.host[i] in contact_hosts:
				contact_hosts.remove(student.host[i])
			# Add to dict
			map_host_to_contacts[student.host[i]] = contact_hosts


		# Remove duplicate elements
		contact_hosts = list(dict.fromkeys(contact_hosts))

		# Add to dict
		map_host_to_contacts[student.host[i]] = contact_hosts

		print(map_host_to_contacts)

		print(contact_hosts)

		i += 1

get_contacts_1(infected_student)