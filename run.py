import sys
import argparse
from datetime import datetime, time, timedelta
from typing import List, Dict

from corona_tracker_42.api42_wrapper import API42
from corona_tracker_42.students import InfectedStudent, Student
from corona_tracker_42.utils.find_contacts import *
from corona_tracker_42.utils.time import *
from corona_tracker_42.utils.checks import *
from corona_tracker_42.utils.print_output import *

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
print("Getting data from the API...")
data = get_data(api, args.day_positive, args.days_to_check)

# Create an object containing information on the student
infected_student = InfectedStudent(args.infected_person_login, args.day_positive, args.days_to_check)

# Get sessions on infected person
get_infected_student_sessions(data, infected_student)

# Get contact hosts from the user
contact_hosts: Dict[str, List[str]] = get_contact_hosts(infected_student, api.campus_id)

# Get contacts (all students who sat on contact hosts during input time range, could also be 0 overlap)
contact_students = get_contacts(data, contact_hosts, infected_student)

# Get the overlap times between the infected person and the contact persons
total_overlap, output = get_overlap_between_contacts(contact_students, contact_hosts, infected_student)

# Sort the output by names
total_overlap = dict(sorted(total_overlap.items()))
output.sort(key = lambda x: x[1])

# Get the person who sat on infected host after infected person sat there
risky_students = get_student_sat_on_infected_host(data, infected_student)

# Output data to out.txt
print_data(total_overlap, output, infected_student, contact_students, risky_students)

# Clear terminal screen
os.system('cls' if os.name == 'nt' else 'clear')

print("See out.txt for the results!")