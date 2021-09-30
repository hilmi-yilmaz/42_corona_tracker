import argparse
import sys
from datetime import datetime, timedelta
from typing import List, Dict

from corona_tracker_42.api42_wrapper import API42
from corona_tracker_42.students import InfectedStudent, Student
from corona_tracker_42.utils import *
from corona_tracker_42.checks import *

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
for session in data:
	if session["user"]["login"] == infected_student.login:
		res = infected_student.append_session(session["id"], session["host"], session["begin_at"], session["end_at"])
		if res == -1: # infected student is currently online
			break

# If no sessions of infected user, exit program
if not infected_student.session_id:
	print("Infected person has no sessions in given time period.")
	sys.exit(1)

# Get contact hosts from the user
contact_hosts: Dict[str, List[str]] = get_contact_hosts(infected_student)

# Get contacts
def get_contacts(data, contact_hosts):
	"""
	Gets the contact hosts.
	"""
	contact_students: List[Student] = []
	for infected_host, contact_host in contact_hosts.items():
		for session in data:
			if session["host"] in contact_host:
				i = is_in_students_list(contact_students, session["user"]["login"])
				if i == -1:
					student = Student(session["user"]["login"])
					student.append_session(session["id"], session["host"], session["begin_at"], session["end_at"])
					contact_students.append(student)
				else:
					contact_students[i].append_session(session["id"], session["host"], session["begin_at"], session["end_at"])

	return (contact_students)

contact_students = get_contacts(data, contact_hosts)

# Get the overlap times between the infected person and the contact persons
total_overlap: Dict[str, int] = {}
for j in range(len(infected_student.session_id)):
	for contact_student in contact_students:
		total_overlap_seconds: int = 0
		for i in range(len(contact_student.session_id)):
			overlap = get_overlap_time(contact_student.begin_at[i], contact_student.end_at[i], infected_student.begin_at[j], infected_student.end_at[j])
			if overlap.days >= 0:
				total_overlap_seconds += overlap.seconds
		if contact_student.login in total_overlap:
			total_overlap[contact_student.login] += total_overlap_seconds
		else:
			total_overlap[contact_student.login] = total_overlap_seconds

total_overlap = {login: overlap for login, overlap in total_overlap.items() if overlap > 0}

for login, overlap in total_overlap.items():
	print("{} logged in for {} next to {}".format(login, str(timedelta(seconds=overlap)), infected_student.login))