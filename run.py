import sys
import argparse
from datetime import datetime, timedelta
from typing import List, Dict

from corona_tracker_42.api42_wrapper import API42
from corona_tracker_42.students import InfectedStudent, Student
from corona_tracker_42.utils.find_contacts import *
from corona_tracker_42.utils.time import *
from corona_tracker_42.utils.checks import *

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

if not check_input(args.day_positive, args.days_to_check):
	sys.exit("Error.\nMake sure your input is correct.")

# Create an API42 object to make calls with
api = API42()

# Get data from the API from the past few days (add one so we can check contact that may have overlap but begin_at is the day before)
data = get_data(api, args.day_positive, args.days_to_check)

# Create an object containing information on the student
infected_student = InfectedStudent(args.infected_person_login, args.day_positive, args.days_to_check)

# Get sessions on infected person
get_infected_student_sessions(data, infected_student)

# Get contact hosts from the user
contact_hosts: Dict[str, List[str]] = get_contact_hosts(infected_student)

# Get contacts
contact_students = get_contacts(data, contact_hosts)

# Get the overlap times between the infected person and the contact persons
total_overlap = get_overlap_between_contacts(contact_students, infected_student)

for login, overlap in total_overlap.items():
	print("{} logged in for {} next to {}".format(login, str(timedelta(seconds=overlap)), infected_student.login))